"""Self-contained Lecture 1 route; leaves the original market state alone."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from calculator import calculate
from lecture_engine import (CASES, STOCK_QUOTES, option_outcome, stock_portfolio,
                            merger_target, merger_portfolio, merger_cost, check_merger)
from studio_theme import style_plotly


def reset_case():
    for k in list(st.session_state):
        if k.startswith('l1_') and k not in ('l1_case',):
            del st.session_state[k]


def changed_case():
    st.query_params['page'] = 'lecture1'
    st.query_params['case'] = st.session_state.l1_case
    reset_case()


def chart(frame, x, columns, ylabel):
    fig = go.Figure()
    for i, c in enumerate(columns):
        fig.add_trace(go.Scatter(x=frame[x], y=frame[c], name=c,
                                line=dict(width=3, dash=['solid','dash','dot'][i%3])))
    fig.update_layout(xaxis_title=x, yaxis_title=ylabel, height=400,
                      legend=dict(orientation='h', y=1.13), margin=dict(t=55,b=45))
    st.plotly_chart(style_plotly(fig), key='l1_chart', width='stretch', theme=None)


def calculator(symbols, definitions, answer_key, text_answer=False):
    with st.expander('Calculator · use numbers or financial symbols', expanded=True):
        st.caption('Optional leading =; +, -, *, /, ^, parentheses, exp, sqrt, min and max. No cell addresses required.')
        st.dataframe(pd.DataFrame([{'Symbol':k,'Meaning':definitions.get(k,k),'Value':v}
                                  for k,v in symbols.items()]), hide_index=True, width='stretch')
        def insert(token):
            st.session_state.l1_expr = st.session_state.get('l1_expr','')+token
        cols=st.columns(min(len(symbols),4))
        for i,k in enumerate(symbols):
            cols[i%len(cols)].button(k, key='l1_insert_'+k, on_click=insert, args=(k,))
        expr=st.text_input('Your calculation',key='l1_expr',placeholder='For example: 30 + 0.50')
        if st.button('Calculate',key='l1_calculate'):
            try:
                result=calculate(expr,symbols)
                st.session_state.l1_calc=(expr,dict(symbols),result)
            except ValueError as e:
                st.session_state.pop('l1_calc',None)
                st.error(str(e))
        saved=st.session_state.get('l1_calc')
        if saved and saved[:2] == (expr,dict(symbols)):
            st.code(expr,language=None)
            st.success(f'Result: {saved[2]:,.6f} (units follow your expression)')
            def transfer():
                st.session_state[answer_key]=saved[0] if text_answer else float(saved[2])
            st.button('Use result as my answer',key='l1_transfer',on_click=transfer)
        elif saved:
            st.caption('Inputs or expression changed. Calculate again before transferring a result.')


def answer(expected, label, explanation):
    if 'l1_answer' not in st.session_state:
        st.session_state.l1_answer = 0.0
    value=st.number_input(label,step=0.0001,format='%.4f',key='l1_answer')
    if st.button('Check my answer',key='l1_check'):
        if abs(value-expected)<=.005:
            st.success('Correct. '+explanation)
        else:
            st.info('Not yet. Check the signs, timing, and units; use a hint or open the worked solution.')


def stock_quotes():
    with st.expander('Lecture quotes and conventions'):
        st.dataframe(pd.DataFrame([{'Strike':k,'Call':v['call'],'Put':v['put']}
                                  for k,v in STOCK_QUOTES.items()]),hide_index=True)
        st.write('Stock today: 30. Six-month European options, one share per option unit. '
                 'Use the supplied two-decimal quotes exactly. Simplified profit subtracts '
                 'initial economic cost without financing. No dividends or transaction costs.')
        st.caption('These fixed lecture quotes do not change the separate model-generated market in the original tools.')


def render_case(case):
    if st.session_state.get('active_example') != case:
        reset_case()
        st.session_state.active_example = case
    st.query_params['page'] = {'single-options':'basics','merger':'replication'}.get(case,'applications')
    st.query_params['case'] = case
    st.button('Reset to lecture example', key='l1_reset', on_click=reset_case)
    if case == 'single-options':
        single_page()
    elif case == 'merger':
        merger_page()
    else:
        portfolio_page(case)


def single_page():
    st.subheader('Does exercising the option mean making a profit?')
    st.write('**Learning objective:** distinguish a contractual payoff from profit, and identify the writer’s obligation.')
    st.write('**Lecture problem (slide 10):** a call has strike 30 and premium 2.89. '
             'At a terminal stock price of 31, calculate the exercise payoff and simplified profit. '
             'Find the break-even price.')
    stock_quotes()
    st.write('Type a number or an expression directly into each answer box, then click Check this answer. You can use ST, K, and premium. Your expression stays visible. The calculator above the answers is optional.')
    targets = {'l1_payoff':'1 · Exercise payoff ($/share)',
               'l1_profit':'2 · Simplified profit ($/share)',
               'l1_breakeven':'3 · Break-even stock price ($/share)'}
    destination = st.selectbox('Send calculator result to', list(targets), format_func=targets.get, key='l1_destination')
    calculator({'ST':31.,'K':30.,'premium':2.89},
               {'ST':'Terminal stock price ($/share)','K':'Strike ($/share)','premium':'Initial premium ($/share)'},destination,text_answer=True)
    for key, expected in [('l1_payoff',1.),('l1_profit',-1.89),('l1_breakeven',32.89)]:
        st.session_state.setdefault(key,'')
        expression=st.text_input(targets[key],key=key,placeholder='Enter a number or expression',
                                 help='Arithmetic, parentheses, max, and the symbols ST, K, premium are supported. A leading = is optional.')
        if st.button('Check this answer',key=key+'_check'):
            if not expression.strip():
                st.info('Enter a number or expression first.')
                continue
            try:
                value=calculate(expression,{'ST':31.,'K':30.,'premium':2.89})
            except ValueError as error:
                st.error(str(error))
                continue
            st.caption(f'Your expression evaluates to {value:,.4f} dollars per share.')
            if abs(value-expected)<=.005:
                st.success('Correct.')
            else:
                st.info('Not yet. Use the hint or reveal the worked solution below.')
    with st.expander('Hint'):
        st.write('For payoff, compare 31 with the strike 30: the call pays the positive difference. For simplified profit, subtract the premium from that payoff. For break-even, find the stock price at which the payoff equals the premium.')
    with st.expander('Reveal the worked solution'):
        st.latex(r'C_T=\max(31-30,0)=1,\qquad \Pi_T=1-2.89=-1.89.')
        st.write('Break-even = 30 + 2.89 = 32.89. The short call has the opposite payoff and profit, ignoring trading frictions.')
    st.success('What we learned: the buyer owns a right, the writer owes the corresponding payoff, and payoff and profit answer different questions.')


def portfolio_page(case):
    specs={
      'protective-put':('Keep the upside, put a floor under the holding',
        'Distinguish a terminal value floor from protection against every loss.',
        'An investor holds one share worth 30 today. She wants at least 25 at expiration while retaining further upside. A 25 put costs 0.50.',
        1.,0.,-5.50,'Your minimum simplified profit ($/share)',
        'Buy one 25 put. The floor is 25; economic commitment is 30 + 0.50 = 30.50. Minimum profit = 25 - 30.50 = -5.50.'),
      'covered-call':('Accept a selling price in return for a premium',
        'Explain why a covered call is not a downside floor.',
        'The investor owns the 30 stock and is willing to surrender terminal value above 35. She sells a 35 call for 1.13.',
        0.,-1.,6.13,'Your maximum simplified profit ($/share)',
        'Sell one 35 call. Terminal value is capped at 35; economic commitment is 30 - 1.13 = 28.87. Maximum profit = 35 - 28.87 = 6.13. Downside remains.'),
      'collar':('Pay for protection by surrendering upside',
        'Build a collar from the desired outcome.',
        'The investor wants a terminal floor of 25, accepts a cap of 35, and wants to reduce the put’s premium cost. Available quotes: 25 put costs 0.50; 35 call costs 1.13.',
        1.,-1.,29.37,'Your initial economic commitment ($/share)',
        'Hold one share, buy one 25 put, sell one 35 call. Option outlay = 0.50 - 1.13 = -0.63 (a receipt). Initial commitment = 29.37. Terminal value is between 25 and 35; profit is between -4.37 and 5.63.'),
    }
    title,obj,problem,put,call,expected,label,solution=specs[case]
    st.subheader(title);st.write('**Learning objective:** '+obj);st.write('**Lecture problem:** '+problem)
    stock_quotes()
    st.caption('The share is already held: its current value is the wealth benchmark, not a second cash purchase today.')
    st.markdown('1. Identify the adverse outcome.\n2. Choose signed option positions.\n3. Sum terminal values.\n4. Compare with the initial economic commitment.')
    calculator({'S0':30.,'KP':25.,'KC':35.,'P25':.50,'C35':1.13},
               {'S0':'Current share value','KP':'Put strike','KC':'Call strike','P25':'25 put premium','C35':'35 call premium'},'l1_answer')
    answer(expected,label,'Keep terminal value and simplified profit separate.')
    with st.expander('Hint'):
        st.write('Long puts add positive value in low-price states. Short calls subtract value in high-price states. Subtract the signed initial cost to obtain simplified profit.')
    with st.expander('Reveal the worked solution'):
        st.write(solution)
        states=[20.,25.,30.,35.,40.]
        rows=[]
        for s in states:
            value,profit,cost=stock_portfolio(s,1,put,call)
            rows.append({'ST':s,'Stock':s,'Put contribution':put*max(25-s,0),
                         'Call contribution':call*max(s-35,0),'Total value':value,'Profit':profit})
        st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
    st.subheader('Explore the trade-off')
    st.caption('Start at the lecture construction. Change quantities to see why partial or excessive hedges alter the result. Positive = long; negative = short.')
    c1,c2=st.columns(2)
    pq=c1.number_input('25 put quantity',min_value=-3.,max_value=3.,value=put,step=.25,key='l1_put_qty')
    cq=c2.number_input('35 call quantity',min_value=-3.,max_value=3.,value=call,step=.25,key='l1_call_qty')
    pts=np.linspace(0,60,121);vals=[stock_portfolio(s,1,pq,cq) for s in pts]
    cost=vals[0][2];st.metric('Initial economic commitment',f'{cost:.2f}')
    st.caption(f'Signed option outlay: {cost-30:.2f}. A negative amount is received today.')
    mode=st.radio('Display',['Terminal value','Simplified profit'],horizontal=True,key='l1_display')
    if mode=='Terminal value':
        frame=pd.DataFrame({'Terminal stock price ($)':pts,'Stock':pts,'Your position':[v[0] for v in vals]})
    else:
        frame=pd.DataFrame({'Terminal stock price ($)':pts,'Stock':pts-30,'Your position':[v[1] for v in vals]})
    chart(frame,'Terminal stock price ($)',['Stock','Your position'],mode+' ($/share)')
    st.caption('The graph shows selected prices, not a bound on possible stock prices or losses. Short-option positions can create substantial obligations.')
    st.success('What we learned: protection, initial premium, and retained upside must be evaluated together. The lecture floor/cap applies to its specified matched positions, not every quantity you can enter.')


def merger_page():
    st.subheader('A merger agreement is a payoff-design problem')
    st.write('**Learning objective:** translate negotiated terms into a terminal payout, replicate it, and value the successful construction.')
    st.write('**Lecture problem (slides 24–29):** let ST be the acquirer’s share price at closing. '
             'Each target share receives 5 + ST below 70; a fixed 75 between 70 and 90; '
             'and 75 + 0.5(ST − 90) above 90. Assume closing and payment occur at T; deal failure risk is excluded.')
    st.latex(r'X_T=\begin{cases}5+S_T&S_T<70\\75&70\leq S_T\leq90\\75+\frac12(S_T-90)&S_T>90.\end{cases}')
    st.info('This is a separate market: S0 = 80, C70 = 13.79, C90 = 3.86. A bond paying 5 at T costs 4.88. All components have matching payment dates. Quotes are supplied; no Black–Scholes calculation is needed.')
    st.markdown('1. Start below 70 with the line 5 + ST.\n2. At 70, change slope from 1 to 0.\n3. At 90, change slope from 0 to 0.5.\n4. Check the payout before valuing the claim.')
    names=['Terminal cash payment','Shares','70 call quantity','90 call quantity']
    keys=['l1_cash','l1_shares','l1_c70','l1_c90']
    st.caption('Enter your construction. Positive quantities are long; negative quantities are short. Use decimal quantities, including 0.5 for half a call.')
    cols=st.columns(4)
    quantities=[cols[i].number_input(name,min_value=-1000.,max_value=1000.,value=0.,step=.5,key=keys[i]) for i,name in enumerate(names)]
    cash,stock,c70,c90=quantities
    if st.button('Check my replication',key='l1_rep_check'):
        st.session_state.l1_attempt=tuple(quantities)
    attempted=st.session_state.get('l1_attempt')==tuple(quantities)
    matched=check_merger(*quantities)
    cost=merger_cost(*quantities)
    if attempted:
        if matched:st.success('Your construction matches every nonnegative terminal stock price. Now value it using the supplied quotes.')
        else:st.info('Not yet. Compare the initial line and the slopes in each region. The cost below is your portfolio’s cost, not the target claim’s value.')
    elif 'l1_attempt' in st.session_state:
        st.caption('Positions changed. Check the new construction again.')
    points=np.unique(np.r_[np.linspace(0,140,141),70,90])
    frame=pd.DataFrame({'Acquirer price at closing ($)':points,'Target payout':[merger_target(s) for s in points],
                        'Your payout':[merger_portfolio(s,*quantities) for s in points]})
    chart(frame,'Acquirer price at closing ($)',['Target payout','Your payout'],'Dollars per target share')
    if attempted:
        states=[0,60,70,80,90,100,110,140]
        st.dataframe(pd.DataFrame([{'ST':s,'Target':merger_target(s),'Your payout':merger_portfolio(s,*quantities),
                                   'Difference':merger_portfolio(s,*quantities)-merger_target(s)} for s in states]),hide_index=True)
        st.metric('No-arbitrage value of matched claim' if matched else 'Cost of your unmatched portfolio',f'{cost:.4f}')
    with st.expander('Hint 1 · start with the first line'):
        st.write('Below 70 both calls expire worthless. Which terminal cash payment and share count give 5 + ST?')
    with st.expander('Hint 2 · change the slopes'):
        st.write('Call quantity = slope to the right − slope to the left. Selling a call removes slope above its strike.')
    calculator({'B':cash,'nS':stock,'n70':c70,'n90':c90,'D':4.88/5,'S0':80.,'C70':13.79,'C90':3.86},
               {'B':'Your terminal cash payment','nS':'Your shares','n70':'Your 70 calls','n90':'Your 90 calls',
                'D':'Price today of $1 at T','S0':'Share price today','C70':'70 call price','C90':'90 call price'},'l1_answer')
    def build_expression():st.session_state.l1_expr='B*D+nS*S0+n70*C70+n90*C90'
    st.button('Build expression from my positions',key='l1_build_expr',on_click=build_expression)
    if attempted and matched:
        answer(73.02,'Your value of the replicated claim ($/target share)','Same payout and payment rights imply the same value under the stated assumptions.')
    else:
        st.caption('The calculator values your positions at any time. The target-value answer check opens after your replication matches.')
    with st.expander('Reveal the full worked solution'):
        st.write('Hold cash paying 5, one share, short one 70 call, and long half a 90 call.')
        st.latex(r'X_T=5+S_T-(S_T-70)^++\frac12(S_T-90)^+.')
        st.write('At 70 and 90 the payout is 75 on both adjacent segments. Below 70 slope is 1; in the middle it is 0; above 90 it is 0.5.')
        st.latex(r'X_0=4.88+80-13.79+\frac12(3.86)=73.02.')
    with st.expander('Further application · change the upper participation'):
        alpha=st.slider('Participation above 90',0.,1.,.5,.1,key='l1_alpha')
        st.write(f'Keep cash 5, one share, and short one 70 call; change the 90 call quantity to {alpha:.1f}. '
                 f'The new initial cost is {merger_cost(5,1,-1,alpha):.2f}. The fixed middle payment stays 75.')
    st.success('What we learned: read the slope changes, reproduce the terminal payout, then value the components. Alternative put-based and middle-first constructions come in Lecture 2.')
