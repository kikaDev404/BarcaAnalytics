import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
import ba_colors_collection.ba_colors as colors
from pre_process import*
import numpy as np

project_root = config.DIR_NAMES.project_root
log_folder = join(project_root, config.DIR_NAMES.log_folder)

log_obj = config_log('mod_el_classico', join(log_folder, 'mod_el_classico.log'), logging.INFO)
log = log_obj.get_logger()



log.info('Trying to rend EL Classico Panel')

def filter_el_classico(df, col_1, col_2):
    df = df.loc[(df[col_1] == 'Real Madrid') | (df[col_2] == 'Real Madrid')]
    return df

@module.ui
def el_classico_ui() -> pd.DataFrame:
    return ui.card(
        ui.card('Overall Classico Result',
            ui.row(
                ui.column(3, ui.value_box('Total played', ui.output_text('total_match_played'), showcase=output_widget('total_played_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Won', ui.output_text('total_match_won'), showcase=output_widget('won_bargraph'),showcase_layout=("bottom"),style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Draw', ui.output_text('total_match_drawed'), showcase=output_widget('draw_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Lost', ui.output_text('total_match_lost'), showcase=output_widget('lost_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;"))
            ),
        ),
        ui.row(
            ui.column(4, ui.card('EL Classico Season Data',ui.output_data_frame('season_summary_data_el_classico'))),
            ui.column(8, ui.card('El Classico Seasonal Result Graph', output_widget('el_classico_seasonal_plot'))),
        ),
        ui.card('Half Time VS Full Time - Barcelona Status', ui.output_ui('halftime_fulltime_dataframe'))
    )

@module.server
def el_classico_server(input,output,session,match_played_place):
    season_data_el_classico = reactive.Value(None)
    count_of_outcomes_el_classico = reactive.Value()

    @render.data_frame
    def season_summary_data_el_classico():
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = barca_data_filtered.loc[(barca_data_filtered['HomeTeam'] == 'Real Madrid') | (barca_data_filtered['AwayTeam'] == 'Real Madrid')]
        temp = barca_data_filtered.groupby(['Match Result', 'Season']).size().reset_index(name = 'Number of games')
        season_data_el_classico.set(temp)
        pivoted = temp.pivot(index='Match Result', columns='Season', values='Number of games').fillna(0).astype(int).reset_index()
        return render.DataGrid(pivoted)
    
    @render_widget
    def el_classico_seasonal_plot():
        fig = plot_bar_graph_stacked(season_data_el_classico(), x_col='Season', y_col='Number of games', log = log, color_col='Match Result', text_col='Number of games', color=colors.ba_sequential_color.barca_sequential_default_colors)

        # for trace in fig.data:
        #     if trace.name == 'Win':
        #          trace.marker.color = colors.ba_single_color.barca_black
        #     elif trace.name == 'Lost':
        #          trace.marker.color = colors.solid_colors.solid_white
        #     elif trace.name == 'Draw':
        #          trace.marker.color = colors.ba_single_color.barca_yellow
        return fig
    
    @render_widget
    def overall_classico_result_plot():
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = barca_data_filtered.loc[(barca_data_filtered['HomeTeam'] == 'Real Madrid') | (barca_data_filtered['AwayTeam'] == 'Real Madrid')]
        temp = barca_data_filtered.groupby(['Match Result']).size().reset_index(name='Number of games')
        fig = plot_bar_graph_stacked(temp, x_col='Number of games', y_col='Match Result', log=log, orientation_type='h', color_col='Match Result', text_col='Number of games',color=colors.ba_sequential_color.barca_sequential_default_colors) 
         

        # for trace in fig.data:
        #     if trace.name == 'Win':
        #             trace.marker.color = colors.ba_single_color.barca_black
        #     elif trace.name == 'Lost':
        #             trace.marker.color = colors.solid_colors.solid_white
        #     elif trace.name == 'Draw':
        #             trace.marker.color = colors.ba_single_color.barca_yellow
    
        return fig
    
    @render.ui
    def halftime_fulltime_dataframe():
        ht_result_score = {'Trailing': -1, 'Draw': 0, 'Lead': 1}
        ft_result_score = {'Lost': -1, 'Draw': 0, 'Win': 1}



        def color_map_draw(df):
            conditions = [
                df['Half Time Result'] == 'Draw',
                df['Half Time Result'] == 'Trailing',
                df['Half Time Result'] == 'Leading'
            ]
            colors = ['Yellow', 'Green', 'Red']
            return pd.Series(np.select(conditions, colors, default='White'), index=df.index)


        # def map_color(df, current_col):
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        temp = barca_data_filtered.groupby(['Half Time Result', 'Match Result']).size().reset_index(name = 'Count')
        pivoted_data = temp.pivot(index='Half Time Result', columns='Match Result', values='Count').fillna(0).astype(int).reset_index()
        

        gt_table = make_gt_table(pivoted_data, log = log)

        gt_table = (
            gt_table
            .tab_style(style=style.fill(color=color_map_draw),locations=loc.body(columns='Draw'))
        )

        gt_table = add_gt_spanner(gt_table, {'Full Time Result' : ['Draw', 'Lost', 'Win']}, log = log)
        gt_table = gt_table.tab_options(table_width="50%")
        return ui.HTML(gt_table.as_raw_html())

    @render_widget
    def total_played_bargraph():
        barca_data_filtered = apply_filter(barca_data, match_played_place(),log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        # Group by Date and Match Result
        temp = (
            barca_data_filtered
            .groupby(['Season'])
            .size()
            .reset_index(name='Number Of Games')
            .sort_values('Season')
        )
        # Plot time series sparkline
        fig = plot_bar_graph(temp,'Season','Number Of Games', log=log)
        fig = conver_bar_plot_for_valuebox(fig,log)
        return fig

    @render_widget()
    def won_bargraph():
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        barca_data_filtered = barca_data_filtered.loc[barca_data_filtered['Match Result'] == 'Win']


        # Group by Date and Match Result
        temp = (
            barca_data_filtered
            .groupby(['Season'])
            .size()
            .reset_index(name='Number Of Games')
            .sort_values('Season')
        )
        # Plot time series sparkline
        fig = plot_bar_graph(temp,'Season','Number Of Games', log=log)
        fig = conver_bar_plot_for_valuebox(fig,log)
        return fig
     
    @render_widget()
    def draw_bargraph():
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        barca_data_filtered = barca_data_filtered.loc[barca_data_filtered['Match Result'] == 'Draw']


        # Group by Date and Match Result
        temp = (
            barca_data_filtered
            .groupby(['Season'])
            .size()
            .reset_index(name='Number Of Games')
            .sort_values('Season')
        )
        # Plot time series sparkline
        fig = plot_bar_graph(temp,'Season','Number Of Games', log=log)
        fig = conver_bar_plot_for_valuebox(fig,log)
        return fig
     
    @render_widget()
    def lost_bargraph():
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        barca_data_filtered = barca_data_filtered.loc[barca_data_filtered['Match Result'] == 'Lost'] 


        # Group by Date and Match Result 
        temp = (
            barca_data_filtered
            .groupby(['Season'])
            .size()
            .reset_index(name='Number Of Games')
            .sort_values('Season')
        )
        # Plot time series sparkline
        fig = plot_bar_graph(temp,'Season','Number Of Games', log=log)
        fig = conver_bar_plot_for_valuebox(fig,log)
        return fig
    
    @render.text
    def total_match_played():
         barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
         barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
         count_outcome = barca_data_filtered.groupby('Match Result').size().reset_index(name='Count')
         total_outcome_count = pd.DataFrame({'Match Result' : 'Total', 'Count' : [count_outcome['Count'].sum()]})

         full_outcome_count = pd.concat([count_outcome, total_outcome_count], ignore_index=True)
         count_of_outcomes_el_classico.set(full_outcome_count)

         total_match_played_count = full_outcome_count.loc[full_outcome_count['Match Result'] == 'Total', 'Count'].values[0]
         
         return str(total_match_played_count)
     
    @render.text
    def total_match_won():
         count_outcomes = count_of_outcomes_el_classico()
         return str(count_outcomes.loc[count_outcomes['Match Result'] == 'Win', 'Count'].values[0])
     
    @render.text
    def total_match_drawed():
         count_outcomes = count_of_outcomes_el_classico()
         draw_df = count_outcomes.loc[count_outcomes['Match Result'] == 'Draw', 'Count']
         return  str(draw_df.values[0]) if not draw_df.empty else "0"
     
    @render.text
    def total_match_lost():
         count_outcomes = count_of_outcomes_el_classico()
         return str(count_outcomes.loc[count_outcomes['Match Result'] == 'Lost', 'Count'].values[0])

    


