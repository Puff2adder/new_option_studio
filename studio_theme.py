"""Course-wide contrast helpers, revision 2. No financial calculations here."""
import streamlit as st

CSS = '''<style>
.stApp {background:#FFFFFF!important;color:#142B49!important;color-scheme:light;}
[data-testid="stSidebar"],[data-testid="stSidebarContent"] {background:#EAF4FF!important;color:#142B49!important;}
[data-testid="stHeader"] {background:#FFFFFF!important;color:#142B49!important;}
[data-testid="stMarkdown"],[data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"],[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label,[data-testid="stSlider"] {color:#142B49!important;}
[data-testid="stMarkdown"] p,[data-testid="stCaptionContainer"] p,
[data-testid="stWidgetLabel"] p,[data-testid="stRadio"] p,
[data-testid="stCheckbox"] p {color:inherit!important;}
h1,h2,h3,h4,h5,h6 {color:#0756A3!important;}
[data-testid="stLatex"],[data-testid="stText"],.katex {color:#142B49!important;}
[data-testid="stMetric"] {background:#EAF4FF!important;color:#142B49!important;}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"] {color:#142B49!important;}
.concept,.why,.success-box,.warning-box,.objective,.callout,.question,.warningbox,.successbox {color:#142B49!important;}
.concept *,.why *,.success-box *,.warning-box *,.objective *,
.callout *,.question *,.warningbox *,.successbox * {color:inherit!important;}
.small-note,.footer {color:#234E70!important;}
.hero,.welcome {background:#123F4C!important;color:#FFFFFF!important;}
.hero *,.welcome * {color:#FFFFFF!important;}
.step {background:#123F4C!important;color:#FFFFFF!important;}
[data-testid="stExpander"] details {background:#FFFFFF!important;color:#142B49!important;}
[data-testid="stExpander"] summary {background:#EAF4FF!important;color:#142B49!important;}
[data-testid="stTable"] {background:#FFFFFF!important;color:#142B49!important;}
[data-testid="stTable"] th {background:#EAF4FF!important;color:#142B49!important;}
[data-testid="stTable"] td {background:#FFFFFF!important;color:#142B49!important;}
/* Pair native fields as well: dark-mode clients must not inherit white ink. */
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {background:#FFFFFF!important;color:#142B49!important;-webkit-text-fill-color:#142B49!important;caret-color:#142B49;}
[data-testid="stTextInput"] input::placeholder,[data-testid="stNumberInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {color:#345575!important;opacity:1;}
[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stTextArea"] [data-baseweb="textarea"] {background:#FFFFFF!important;color:#142B49!important;}
[data-baseweb="select"]>div {background:#FFFFFF!important;color:#142B49!important;}
[data-baseweb="select"] input {color:#142B49!important;-webkit-text-fill-color:#142B49!important;}
[data-baseweb="select"] svg {fill:#142B49!important;}
[role="listbox"],[role="option"] {background:#FFFFFF!important;color:#142B49!important;}
[role="option"][aria-selected="true"],[role="option"]:hover {background:#EAF4FF!important;color:#142B49!important;}
[data-testid="stButton"] button,[data-testid="stDownloadButton"] button,
[data-testid="stFormSubmitButton"] button,[data-testid="stNumberInput"] button {
background:#EAF4FF!important;color:#142B49!important;border-color:#54799B!important;}
[data-testid="stButton"] button p,[data-testid="stDownloadButton"] button p,
[data-testid="stFormSubmitButton"] button p {color:inherit!important;}
[data-testid="stButton"] button:hover,[data-testid="stFormSubmitButton"] button:hover {background:#D7EAFB!important;}
[data-testid="stButton"] button:disabled {opacity:.65;}
[data-testid="stTabs"] button {color:#142B49!important;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#0756A3!important;}
/* Alerts have their own native background: inherit its native foreground. */
[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stAlert"] p {color:inherit!important;}
</style>'''

def apply_studio_theme():
    st.markdown(CSS, unsafe_allow_html=True)

def style_plotly(fig):
    """Set the figure surface and labels together; preserve data and trace colors."""
    fig.update_layout(template='plotly_white',paper_bgcolor='#FFFFFF',
                      plot_bgcolor='#FFFFFF',font_color='#142B49',
                      legend_font_color='#142B49', title_font_color='#142B49')
    fig.update_xaxes(color='#142B49',gridcolor='#D4E2EF')
    fig.update_yaxes(color='#142B49',gridcolor='#D4E2EF')
    return fig

def studio_line_chart(data, *, color=None, x_label=None, y_label=None, **kwargs):
    """Light Vega chart for the studios' wide numeric dataframes."""
    import altair as alt
    frame=data.copy()
    index_name=frame.index.name or 'Index'
    frame.index.name=index_name
    frame=frame.reset_index().melt(id_vars=[index_name],var_name='Series',value_name='Value')
    encoding=alt.Color('Series:N',legend=alt.Legend(title=None))
    if color:
        encoding=alt.Color('Series:N',scale=alt.Scale(range=color if isinstance(color,list) else [color]),legend=alt.Legend(title=None))
    chart=alt.Chart(frame).mark_line().encode(x=alt.X(f'{index_name}:Q',title=x_label or index_name),
            y=alt.Y('Value:Q',title=y_label or 'Value'),color=encoding).configure(
            background='#FFFFFF').configure_axis(labelColor='#142B49',titleColor='#142B49',
            gridColor='#D4E2EF').configure_legend(labelColor='#142B49',titleColor='#142B49')
    return st.altair_chart(chart,theme=None,use_container_width=True,**kwargs)

WORKSHEET_CSS = '''<style id="course-theme-contrast">
html {color-scheme:light;}body {background:#FFFFFF;color:#142B49;}
input,textarea,select {background:#FFFFFF;color:#142B49;caret-color:#142B49;}
input::placeholder,textarea::placeholder {color:#345575;opacity:1;}
.formula input {background:#FFFFFF!important;color:#142B49!important;}
option {background:#FFFFFF;color:#142B49;}
</style>'''
