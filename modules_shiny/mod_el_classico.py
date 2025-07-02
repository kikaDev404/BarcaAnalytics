import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
import ba_colors_collection.ba_colors as colors
from pre_process import*

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
        ui.card('Overall Classico Result', output_widget('overall_classico_result_plot')),
        ui.row(
            ui.column(4, ui.card('EL Classico Season Data',ui.output_data_frame('season_summary_data_el_classico'))),
            ui.column(8, ui.card('El Classico Seasonal Result Graph', output_widget('el_classico_seasonal_plot'))),
        ),
        ui.card('Half Time VS Full Time - Barcelona Status', ui.output_ui('halftime_fulltime_dataframe'))
    )

@module.server
def el_classico_server(input,output,session,match_played_place):
    season_data_el_classico = reactive.Value(None)

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

        # def map_color(df, current_col):
        barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
        barca_data_filtered = filter_el_classico(barca_data_filtered, 'HomeTeam', 'AwayTeam')
        temp = barca_data_filtered.groupby(['Half Time Result', 'Match Result']).size().reset_index(name = 'Count')
        pivoted_data = temp.pivot(index='Half Time Result', columns='Match Result', values='Count').fillna(0).astype(int).reset_index()

        gt_table = make_gt_table(pivoted_data, log = log)
        gt_table = add_gt_spanner(gt_table, {'Full Time Result' : ['Draw', 'Lost', 'Win']}, log = log)
        gt_table = gt_table.tab_options(table_width="50%")
        return ui.HTML(gt_table.as_raw_html())

    


