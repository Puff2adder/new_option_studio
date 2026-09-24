"""Lecture 1 supplied quotes and pure terminal-payoff calculations.

These rounded classroom quotes are inputs, not outputs of a pricing model.
The merger is a separate market from the S0=30 insurance examples.
"""
from math import isfinite

STOCK_QUOTES = {25: {'call': 6.11, 'put': .50},
                30: {'call': 2.89, 'put': 2.15},
                35: {'call': 1.13, 'put': 5.26}}
CASES = {
    'single-options': '1 · Option rights, payoff and profit',
    'protective-put': '2 · Protect the holding',
    'covered-call': '3 · Exchange upside for premium',
    'collar': '4 · Design a floor and a cap',
    'merger': '5 · Replicate the merger payout',
}


def option_outcome(terminal, strike=30, kind='call', side=1):
    if strike not in STOCK_QUOTES or kind not in ('call', 'put') or side not in (-1, 1):
        raise ValueError('Choose an available strike, call/put and long/short side.')
    if not isfinite(terminal) or terminal < 0:
        raise ValueError('Enter a nonnegative finite stock price.')
    payoff = side * max(terminal-strike if kind == 'call' else strike-terminal, 0)
    cost = side * STOCK_QUOTES[strike][kind]
    return payoff, payoff-cost, cost


def stock_portfolio(terminal, stock=1., puts=0., calls=0.):
    """One-share units; put K25 and call K35; premiums not financed."""
    if any(not isfinite(v) for v in (terminal, stock, puts, calls)) or terminal < 0:
        raise ValueError('Use finite quantities and a nonnegative stock price.')
    cost = 30*stock + .50*puts + 1.13*calls
    payoff = stock*terminal + puts*max(25-terminal, 0) + calls*max(terminal-35, 0)
    return payoff, payoff-cost, cost


def merger_target(terminal):
    if terminal < 70:
        return 5+terminal
    if terminal <= 90:
        return 75.
    return 75+.5*(terminal-90)


def merger_portfolio(terminal, cash, stock, call70, call90):
    return cash+stock*terminal+call70*max(terminal-70, 0)+call90*max(terminal-90, 0)


def merger_cost(cash, stock, call70, call90):
    return cash*(4.88/5)+stock*80+call70*13.79+call90*3.86


def check_merger(cash, stock, call70, call90, tolerance=1e-7):
    values = (cash, stock, call70, call90)
    if any(not isfinite(v) for v in values):
        raise ValueError('Quantities must be finite.')
    # Matching the affine segment intercept/slopes establishes equality on the
    # full nonnegative domain, not merely on a finite plotted interval.
    residuals = (cash-5, stock-1, stock+call70, stock+call70+call90-.5)
    return all(abs(v) <= tolerance for v in residuals)
