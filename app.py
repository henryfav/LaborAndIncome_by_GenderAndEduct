import pandas as pd
import re



data = pd.read_csv('tabn502.20.csv', header = None, names=['Total','Total std', 'Less than 9th grade','Less than 9th grade std', 'Some high school, no completion','Some high school, no completion std','High school completion','High school completion std','Some college, no degree','Some college, no degree std','Associate Degree','Associate Degree std', 'Total higher','Total higher std','Bachelor Degree','Bachelor Degree std','Master Degree','Master Degree std','Professional degree','Professional degree std','Doctor Degree','Doctor Degree std'],index_col=0, skiprows=8, skipfooter = 12)

data = data[data.index.notnull()]

for i in data.columns:
    data[i] = data[i].astype(str)
    data[i] = data[i].replace('-','',regex=True)
#for i in data.columns:
#    if 'std' in i:
#        data[i] = data[i].abs()

#cols = data.columns
#data[cols] = data[cols].apply(pd.to_numeric)
data['Values'] = ''
data.iloc[:46,-1] = 'Current Dollars'
data.iloc[46:92,-1] = 'Real Income'
data.iloc[92:138,-1]='Number of persons with earnings who worked full time, year round (in thousands)'
data.iloc[138:,-1] = 'Percent of workers who are full-time'
df = data.reset_index()
df = df.set_index(['Values','index'])
df.replace(to_replace = [int(0), float(0), str(0)], method='bfill', inplace=True)
#df = pd.read_csv('moo.csv')


df_male = df.iloc[1:23]
moo = df.iloc[47:69]
df_male = df_male.append(moo)
moo = df.iloc[93:115]
df_male = df_male.append(moo)
moo = df.iloc[139:159]
df_male = df_male.append(moo)

df_fem =  df.iloc[24:46]
moo = df.iloc[70:92]
df_fem = df_fem.append(moo)
moo = df.iloc[116:138]
df_fem = df_fem.append(moo)
moo = df.iloc[160:]
df_fem = df_fem.append(moo)
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server

app.layout = html.Div([

        html.Div([
            html.Textarea(
            id = 'title',
            children = 'HOW DOES INCOME, FULL-TIME EMPLOYMENT OPPORTUNITIES VARY BY GENDER AND EDUCATION LEVEL?',

            rows = 6,
            disabled = True,
            readOnly = True,
            style={'width' : '100%','float':'right','font-size':33, 'font-family':'Helvetica','font-weight':'bold', 'border-color': 'rgba(0, 0, 0, 0)', 'resize': 'none',  'text-align': 'center','background-color':'#faf2dc'}),

            html.Textarea(
            id = 'description',
            children = 'Below, choose income or full-time participation rate. Then, select two demographics you are interested in! \n We\'ve also included error bars so you know how much our estimations could be off by.',
            rows = 4,
            disabled = True,
            readOnly = True,
            style={'width' : '100%','font-size':15, 'border-color': 'rgba(0, 0, 0, 0)', 'resize': 'none', 'text-align': 'center','background-color':'#faf2dc'}),



            html.Div([
                dcc.Dropdown(
                    ['Real Income', 'Percent of workers who are full-time'],
                    'Real Income',
                    id = 'metric',
                    clearable = False
                )],
                style={'width': '96%', 'float':'right', 'display': 'inline-block', 'border-color': 'rgba(0, 0, 0, 0)'}),


            html.Div([
                dcc.Dropdown(
                    ['Less than 9th grade',
               'Some high school, no completion', 'High school completion',
               'Some college, no degree', 'Associate Degree',
               'Bachelor Degree',
               'Master Degree','Professional degree',
               'Doctor Degree'],
                    'High school completion',
                    id = 'yaxis-column1',
                    clearable = False
                ),
                dcc.RadioItems(
                        ['Female', 'Male'],
                        'Female',
                        id='yaxis-type1',
                        inline=True),
                dcc.RadioItems(
                        ['Show', 'Hide'],
                        'Show',
                        id='show1')
            ],style={'width': '48%', 'float':'right', 'display': 'inline-block', 'border-color': 'rgba(0, 0, 0, 0)'}),

            html.Div([
                dcc.Dropdown(
                    ['Less than 9th grade',
               'Some high school, no completion', 'High school completion',
               'Some college, no degree', 'Associate Degree',
               'Bachelor Degree',
               'Master Degree','Professional degree',
               'Doctor Degree'],
                    'Bachelor Degree',
                    id = 'yaxis-column2',
                    clearable = False
                ),
                dcc.RadioItems(
                        ['Female', 'Male'],
                        'Female',
                        id='yaxis-type2',
                        inline=True)
            ],style={'width': '48%', 'float':'right','display': 'inline-block', 'border-color': 'rgba(0, 0, 0, 0)'})],
            style={'width':'35%','float':'left', 'height':'auto'}),

        html.Div([
            dcc.Graph(id='graph'),
    ],style={'width': '65%','float':'right',})],
    style={'border': 'thin solid black','overflow':'auto','background-color':'#faf2dc'})


@app.callback(
    Output('graph', 'figure'),
    #Output('title', 'text'),
    Input('metric', 'value'),

    Input('yaxis-column1', 'value'),
    Input('yaxis-type1', 'value'),

    Input('yaxis-column2', 'value'),
    Input('yaxis-type2', 'value'),
    Input('show1','value'))


def update_graph(metric, yaxis_column1, yaxis_type1, yaxis_column2, yaxis_type2, show1):



    if show1 == 'Hide':
        if yaxis_type2 =='Female':
            df = df_fem[df_fem.index.get_level_values(0) == metric]
            fig = px.line(df,
                         x=df.index.get_level_values(1),
                         y = yaxis_column2,
                         error_y = yaxis_column2 + ' std',
                         )
        else:
            df = df_male[df_male.index.get_level_values(0) == metric]
            fig = px.line(df,
                         x=df.index.get_level_values(1),
                         y = yaxis_column1,

                         error_y = yaxis_column1 + ' std',
                         )


    # elif show1 =='Hide' and show2 == 'Show':
    #     if yaxis_type2 =='Female':
    #         df = df_fem[df_fem.index.get_level_values(0) == metric]
    #         fig = px.line(df,
    #                  x=df.index.get_level_values(1),
    #                  y = yaxis_column2,
    #                  error_y = yaxis_column2 + ' std',
    #                  )
    #     else:
    #         df = df_male[df_male.index.get_level_values(0) == metric]
    #         fig = px.line(df,
    #                  x=df.index.get_level_values(1),
    #                  y = yaxis_column1,
    #
    #                  error_y = yaxis_column1 + ' std',
    #                  )


    else:
        df=''
        if yaxis_type1 == 'Female':
            df = df_fem[df_fem.index.get_level_values(0) == metric]
            df = df[[yaxis_column1, yaxis_column1 + ' std']]
            df['Demographic'] = 'Female with ' + yaxis_column1
        else:
            df = df_male[df_male.index.get_level_values(0) == metric]
            df = df[[yaxis_column1, yaxis_column1 + ' std']]
            df['Demographic'] = 'Male with ' + yaxis_column1

        if yaxis_type2 == 'Female':
            data = df_fem[df_fem.index.get_level_values(0) == metric]
            data = data[[yaxis_column2, yaxis_column2 + ' std']]
            data['Demographic'] = 'Female with ' + yaxis_column2
        else:
            data = df_male[df_male.index.get_level_values(0) == metric]
            data = data[[yaxis_column2, yaxis_column2 + ' std']]
            data['Demographic'] = 'Male with ' + yaxis_column2
        data = data.rename({yaxis_column2:yaxis_column1, yaxis_column2 + ' std':yaxis_column1 + ' std'},axis=1)
        df = pd.concat([data,df])


        fig = px.line(df,
                 x=df.index.get_level_values(1),
                 y = yaxis_column1,
                 error_y = yaxis_column1 + ' std',
                 color = 'Demographic'
                 )
    #else:
        #print('hello')
    fig.update_layout(
    xaxis_title="Year",
    yaxis_title=metric,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(x=0,y=-.4))

#    fig.add_vline(fillcolor='black')

    fig.update_yaxes(showgrid=True, gridwidth=.5,gridcolor='lightgreen')
    fig.update_xaxes(showgrid=True, gridwidth=.5, gridcolor='lightgreen')

    if metric == 'Real Income':
        fig.update_layout(yaxis_tickprefix = '$')
    else:
        fig.update_layout(yaxis_ticksuffix = '%')

    fig.update_layout(autotypenumbers='convert types')

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
