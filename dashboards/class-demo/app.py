"""Deployable class demo. Run locally with python app.py or host on Render."""
from dash import Dash, Input, Output, dcc, html
import plotly.express as px
import pandas as pd


def build_dashboard(data):
    data = data.copy()
    devices = ['Non-electric bicycle', 'E-bike', 'Unpowered scooter', 'Powered scooter']
    powered = {'E-bike', 'Powered scooter'}
    bikes = {'Non-electric bicycle', 'E-bike'}
    colors = dict(zip(devices, ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']))
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1('Children, bikes, and scooters: recorded injury patterns'),
        html.P('2025 NEISS sample, ages 5–17. These patterns do not measure injury risk per rider.'),
        html.Label('Patient ages — updates all figures and the table', htmlFor='ages'),
        dcc.RangeSlider(id='ages', min=5, max=17, step=1, value=[5, 17],
                        marks={age: str(age) for age in range(5, 18)}, allowCross=False),
        html.Div([
            html.Div('Power'),
            dcc.RadioItems(id='power', options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Powered', 'value': 'powered'},
                {'label': 'Unpowered', 'value': 'unpowered'}
            ], value='all', inline=True, inputStyle={'marginRight': '6px'},
                labelStyle={'marginRight': '20px'}),
            html.Div('Device', style={'marginTop': '12px'}),
            dcc.RadioItems(id='device', options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Bike', 'value': 'bike'},
                {'label': 'Scooter', 'value': 'scooter'}
            ], value='all', inline=True, inputStyle={'marginRight': '6px'},
                labelStyle={'marginRight': '20px'}),
            html.P('Age, power, and device selections update all figures and the table.')
        ], style={'marginTop': '24px'}),
        html.P(id='sample-summary'),
        dcc.Graph(id='shares'),
        dcc.Graph(id='ages-plot'),
        dcc.Graph(id='care'),
        dcc.Graph(id='care-percent'),
        html.H2('Additional care within each device group'),
        html.Div(id='care-table'),
        html.P('Source: CPSC NEISS, prepared unweighted cases. No national totals or rider/trip denominators. '
               'The additional-care category includes admission, transfer, observation, and fatalities; '
               'False does not establish a mild outcome. 97 overlapping-device records were excluded. '
               'Powered scooter is the source category, not exclusively electric.')
    ], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f3f5f7',
              'color': '#202b35', 'padding': '24px', 'maxWidth': '1100px', 'margin': 'auto'})

    @app.callback(Output('shares', 'figure'), Output('ages-plot', 'figure'),
                  Output('care', 'figure'), Output('care-percent', 'figure'), Output('care-table', 'children'),
                  Output('sample-summary', 'children'), Input('ages', 'value'),
                  Input('power', 'value'), Input('device', 'value'))
    def update_dashboard(ages, power, device):
        visible_devices = [name for name in devices
                           if (power == 'all' or (name in powered) == (power == 'powered'))
                           and (device == 'all' or (name in bikes) == (device == 'bike'))]
        selected = data.loc[data['age'].between(*ages) & data['device_type'].isin(visible_devices)]
        summary = selected.groupby('device_type').agg(cases=('case_number', 'size'),
                                                      care_cases=('additional_care', 'sum'))
        summary = summary.reindex(visible_devices, fill_value=0).reset_index()
        conditional = pd.crosstab(selected['device_type'], selected['additional_care'], normalize='index') * 100
        conditional = conditional.reindex(index=visible_devices, columns=[False, True], fill_value=0)
        summary['care_percent'] = conditional[True].to_numpy()
        summary.loc[summary['cases'].eq(0), 'care_percent'] = float('nan')
        shares = px.bar(summary, x='device_type', y='cases', color='device_type',
                        color_discrete_map=colors, hover_data=['cases'],
                        labels={'device_type': 'Device type', 'cases': 'Cases in dataset'},
                        title='Recorded cases by device type')
        counts = selected.groupby(['age', 'device_type']).size().reindex(
            pd.MultiIndex.from_product([range(ages[0], ages[1] + 1), visible_devices],
                                       names=['age', 'device_type']), fill_value=0).reset_index(name='cases')
        age_plot = px.line(counts, x='age', y='cases', color='device_type',
                          color_discrete_map=colors, category_orders={'device_type': visible_devices},
                          labels={'age': 'Patient age (years)', 'cases': 'Cases in dataset'},
                          title='Recorded cases by age')
        age_plot.update_layout(legend={'x': 1.02, 'y': 1, 'xanchor': 'left'}, margin={'r': 210})
        care_counts = selected.groupby(['device_type', 'additional_care']).size().reindex(
            pd.MultiIndex.from_product([visible_devices, [False, True]],
                                       names=['device_type', 'additional_care']), fill_value=0).reset_index(name='cases')
        care_counts['additional_care'] = care_counts['additional_care'].map({False: 'No additional care', True: 'Additional care required'})
        care = px.bar(care_counts, x='device_type', y='cases', color='additional_care', barmode='group',
                      color_discrete_map={'No additional care': '#1f77b4', 'Additional care required': '#9467bd'},
                      labels={'device_type': 'Device type', 'cases': 'Cases in dataset',
                              'additional_care': 'Additional-care category'},
                      title='Recorded additional-care outcomes')
        care_percent_plot = px.bar(summary, x='device_type', y='care_percent', color='device_type',
                                   color_discrete_map=colors, hover_data=['cases', 'care_cases'],
                                   labels={'device_type': 'Device type', 'care_percent': 'Additional care within device (%)'},
                                   title='Conditional additional-care percentages')
        rows = [html.Tr([html.Th(label) for label in
                         ['Device', 'All cases', 'No additional care', 'Additional care required', 'Additional care within device (%)']])]
        for row in summary.itertuples():
            percent = f'{row.care_percent:.2f}%' if pd.notna(row.care_percent) else 'Not defined (no cases)'
            rows.append(html.Tr([html.Td(value, style={'padding': '8px'}) for value in
                                [row.device_type, row.cases, row.cases - row.care_cases, row.care_cases, percent]]))
        for figure in [shares, age_plot, care, care_percent_plot]:
            figure.update_layout(template='plotly_white', height=460)
        message = f'{len(selected):,} included cases. Ages {ages[0]}–{ages[1]}; power: {power}; device: {device}.'
        if selected.empty:
            message += ' No cases in this selection; within-device percentages are undefined.'
        return shares, age_plot, care, care_percent_plot, html.Table(rows), message

    return app

# Resolve data relative to this file, even when launched from another folder.
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'cpsc_neiss_school_age_micromobility_2025.csv'
injuries_df = pd.read_csv(DATA_PATH, parse_dates=['treatment_date'])
app = build_dashboard(injuries_df)
server = app.server

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8054, debug=False)
