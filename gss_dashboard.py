import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Theme
external_stylesheets=[dbc.themes.SOLAR]

# Data
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"],
                 low_memory=False)

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

replace_map = {'mod. satisfied': 'moderately satisfied', 'a little dissat': 'a little dissatisfied'}
gss_clean['satjob'] = gss_clean['satjob'].replace(replace_map)

# Agreement columns
agree_cols = ['satjob', 'relationship', 'male_breadwinner', 'men_betteresuited', 'child_suffer', 'men_overwork']

# Continuous columns
group_cols = ['sex','region','education']

# Non-changeable figures
## Table
p2 = round(gss_clean.groupby('sex').agg({'income': 'mean',
                                   'job_prestige': 'mean', 
                                   'socioeconomic_index': 'mean',
                                   'education': 'mean'}),2).reset_index()
p2.columns = ['Sex', 'Income', 'Occupational Prestige', 'Socioeconomic Status', 'Years of Education']

table = ff.create_table(p2)

## Scatterplot
fig_p4 = px.scatter(gss_clean, x='job_prestige', y='income', color='sex',
                 hover_data=['education', 'socioeconomic_index'],
                 trendline='lowess',
                 color_discrete_map={'male': '#9467bd',
                                 'female': '#bcbd22'})
fig_p4.update_yaxes(title='Income')
fig_p4.update_xaxes(title='Occupational Prestige')

## Box plots
fig_p5_1 = px.box(gss_clean, x='income', color='sex',
                  color_discrete_map={'male': '#9467bd',
                                 'female': '#bcbd22'})
fig_p5_1.update_layout(showlegend=False)
fig_p5_1.update_xaxes(title='Income')

fig_p5_2 = px.box(gss_clean, x='job_prestige', color='sex',
                  color_discrete_map={'male': '#9467bd',
                                 'female': '#bcbd22'})
fig_p5_2.update_layout(showlegend=False)
fig_p5_2.update_xaxes(title='Occupational Prestige')

# Facet box plots
p6 = round(gss_clean[['income', 'sex', 'job_prestige']].dropna(),2)
p6['job_prestige_binned'] = pd.cut(p6.job_prestige,
                                   bins=6,
                                   labels=['Very low prestige', 'Low prestige', 'Mid-low prestige',
                                           'Mid-high prestige', 'High prestige', 'Very high prestige'])

fig_p6 = px.box(p6, x='sex', y='income', color='sex',
             facet_col='job_prestige_binned',
             facet_col_wrap=2,
             color_discrete_map={'male': '#9467bd',
                                 'female': '#bcbd22'},
             category_orders={'job_prestige_binned': ['Very low prestige', 'Low prestige',
                                                      'Mid-low prestige','Mid-high prestige',
                                                      'High prestige', 'Very high prestige']},
             width=1000, height=1000)
fig_p6.update_layout(showlegend=True)
fig_p6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_binned=", "")))

# Introduction text
markdown_text = """
The gender pay gap is the systemic difference in pay between men and women. In the United States, this difference is usually 
simplified to saying that women earn 84 cents on the dollar compared to men. However, as Allison Elias states in an interview from the 
article *Why the Gender Pay Gap Persists in American Businesses*, this "statistic provides an incomplete picture of women’s
experiences in the labor market since the gap is exacerbated for many women of color. Hispanic and Black women 
experience the largest gaps relative to white, non-Hispanic men...Important to note is that even though women in the 
highest-paid work face the highest wage gap penalties, in general women remain overrepresented in the lowest-paying occupations. 
And occupations with greater proportions of women tend to pay less even when controlling for educational and skill requirements"(1). 

Understanding and addressing this issue is an incredibly important social issue. Unsurprisingly, acknowledgement of and concern about the gender pay
gap varies across political, economic, and other social divides. To also understand these divisions in opinion, we can turn to the GSS. 
The GSS (General Social Survey) is a nationally representative survey of US adults examining a wide range of attitudes
and beliefs related to civil liberties, morality, national spending priorities, and many others. It is a tool that "allows researchers
to examine the structure and functioning of society in general"(2).

---
Sources:

(1) https://news.darden.virginia.edu/2024/04/04/why-the-gender-pay-gap-persists-in-american-businesses/

(2) https://gss.norc.org/About-The-GSS
"""

# Variable explanation
var_explanation = """
The GSS data contains the following features:

* `id` - a numeric unique ID for each person who responded to the survey
* `weight` - survey sample weights
* `sex` - male or female
* `education` - years of formal education
* `region` - region of the country where the respondent lives
* `age` - age
* `income` - the respondent's personal annual income
* `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
* `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
* `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
* `socioeconomic_index` - an index measuring the respondent's socioeconomic status
* `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
* `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
* `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
* `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
* `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
* `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

On subsequent pages, you will be able to actively explore the GSS data using these features. You can refer back to this page for reference.
"""

# Instructions for interactive graph
interact_instruct = """
The below barchart can be updated in real-time by you! By selecting variables from the dropdowns below, you can choose how you would like to explore the data.
The option on the left controls which question you would like to view response for. Your options are:
* `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
* `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
* `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
* `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
* `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
* `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."


The option on the right controls how you would like the responses to be grouped. Your options are:
* `sex` - male or female
* `education` - years of formal education
* `region` - region of the country where the respondent lives

Have fun exploring the data yourself!
"""

# Note
note = """
---
Hello! My name is Isaac Levy and I am a Master's student in UVA's School of Data Science. This dashboard was made as part of Professor Jonathan Kropko's DS6001 course in summer 2024. 

My GitHub profile can be found here: https://github.com/i-levy

My LinkedIn can be found here: https://www.linkedin.com/in/isaac-m-levy/

Thanks Professor Kropko for a great summer!
"""
# Initialize
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Isaac's Viz"


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2("Introduction", className="card-text"),
            dcc.Markdown(markdown_text),
            dcc.Markdown('---'),
            html.H2("Overview of the Data", className="card-text"),
            dcc.Markdown(var_explanation),
            dcc.Markdown(note)
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2("Visualizing the Differences in Income, Prestige, Education, and Socieconomic Status Between Women and Men", className="card-text"),
            html.Div([
                dcc.Markdown("Differences in Demographics Between Men and Women:"),
                dcc.Graph(figure=table),
                ]),
            html.Div([
                html.P(),
                dcc.Markdown("Visualizing Occupational Prestige and Income for Men vs. Women"),
                dcc.Graph(figure=fig_p4)]),
            html.Div([
                html.P(),
                dcc.Markdown("Distribution of Income for Men vs Women"),
                dcc.Graph(figure=fig_p5_1)],
                     style={'width': '48%', 'float': 'left'}),
            html.Div([
                html.P(),
                dcc.Markdown("Distribution of Occupational Prestige for Men vs Women"),
                dcc.Graph(figure=fig_p5_2)],
                     style={'width': '48%', 'float': 'right'}),
            html.Div([
                html.P("\n"),
                dcc.Markdown("Distribution of Income Broken Down by Occupational Prestige for Men vs Women"),
                dcc.Graph(figure=fig_p6)])
        ]
    ),
    className='mt-3'
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2("Exploring the Data Yourself", className="card-text"),
            dcc.Markdown(interact_instruct),
            html.Div([
                html.Div([
                    dcc.Markdown('Please select a question from the options below:'),
                    dcc.Dropdown(id='var_agree',
                                       options=agree_cols,
                                       value='satjob')],
                         style={'width': '48%', 'float': 'left'}),
                html.Div([
                    dcc.Markdown('PLease select a grouping variable from the options below:'),
                    dcc.Dropdown(id='var_group',
                                       options=group_cols,
                                       value='sex')],
                         style={'width': '48%', 'float': 'right'})]),
            html.Div([
                html.P(),
                dcc.Graph(id='box')],
                     style={'width': '98%', 'float': 'right'})
        ]
    ),
    className="mt-3",
)

# Populate
app.layout = html.Div(
    [
        html.H1(["Exploring the 2019 General Social Survey"]),
        
        dcc.Tabs([
            dcc.Tab(tab1_content, label='Introduction'),
            dcc.Tab(tab2_content, label='Getting Started'),
            dcc.Tab(tab3_content, label='Exploring Deeper')
        ])
    ]
)

@app.callback(Output(component_id='box', component_property='figure'),
              [Input(component_id='var_agree', component_property='value'),
               Input(component_id='var_group', component_property='value')])

def makeborplots(x, group):
    p3 = gss_clean[[group, x]].dropna().value_counts().reset_index()
    fig_p3 = px.bar(p3, x=x, y='count', color=group, barmode='group',
             category_orders={'satjob': ['very satisfied', 'moderately satisfied', 'a little dissatisfied', 'very dissatisfied'],
                              'relationship': ['strongly agree', 'agree','disagree', 'strongly disagree'],
                              'male_breadwinner': ['strongly agree', 'agree','disagree', 'strongly disagree'],
                              'men_bettersuited': ['agree', 'disagree'],
                              'child_suffer': ['strongly agree', 'agree','disagree', 'strongly disagree'],
                              'men_overwork': ['strongly agree', 'agree','disagree', 'strongly disagree']
                              })
    
    #fig_p3.update_layout(showlegend=False)
    fig_p3.update_yaxes(title='Count')
    fig_p3.update_xaxes(title='Response')
    return fig_p3

# Run
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)