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

@module.ui
def el_classico_ui():
    return ui.card(
        ui.row(
            ui.column(5, ui.card('EL Classico Season Data',ui.output_data_frame('season_summary_data_el_classico'))),
            ui.column(7, ui.card('El Classico Seasonal Result Graph', output_widget('el_classico_seasonal_plot')))
        )
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
        fig = plot_bar_graph_stacked(season_data_el_classico(), x_col='Season', y_col='Number of games', log = log, color_col='Match Result', text_col='Number of games')

        for trace in fig.data:
            if trace.name == 'Win':
                 trace.marker.color = colors.ba_single_color.barca_black
            elif trace.name == 'Lost':
                 trace.marker.color = colors.solid_colors.solid_white
            elif trace.name == 'Draw':
                 trace.marker.color = colors.ba_single_color.barca_yellow
        return fig