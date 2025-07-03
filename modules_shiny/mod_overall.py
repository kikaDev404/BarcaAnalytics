import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
import ba_colors_collection.ba_colors as colors
from pre_process import*
import faicons

import plotly.express as px

project_root = config.DIR_NAMES.project_root
log_folder = join(project_root, config.DIR_NAMES.log_folder)

log_obj = config_log('mod_overall', join(log_folder, 'mod_overall.log'), logging.INFO)
log = log_obj.get_logger()



log.info('Trying to rend Overall Panel')

@module.ui
def overall_panel():
    return ui.card(
        'An Over view of the Game Barca Played from 2000 to 2025',
        ui.card(
            ui.row(
                ui.column(3, ui.value_box('Total played', ui.output_text('total_match_played'), showcase=output_widget('total_played_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Won', ui.output_text('total_match_won'), showcase=output_widget('won_bargraph'),showcase_layout=("bottom"),style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Draw', ui.output_text('total_match_drawed'), showcase=output_widget('draw_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;")),
                ui.column(3,ui.value_box('Lost', ui.output_text('total_match_lost'), showcase=output_widget('lost_bargraph'),showcase_layout="bottom",style="height: 200px; width: 100%;"))
            ),
        ),
        ui.card(
            ui.row(
                ui.column(
                    4, ui.card('Over All Data', ui.output_data_frame('barca_num_of_match_played_overall'), style='height: 400px; overflow-y: auto;')
                ),
                ui.column(
                    8, ui.card(output_widget('overall_match_bar_graph'), style='height: 400px;')
                ),
            )
        )
    )

@module.server
def overall_panel_server(input,output,session,match_played_place):
     year_data = reactive.Value()
     count_of_outcomes = reactive.Value()
     
     @render.text
     def total_match_played():
         barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
         count_outcome = barca_data_filtered.groupby('Match Result').size().reset_index(name='Count')
         total_outcome_count = pd.DataFrame({'Match Result' : 'Total', 'Count' : [count_outcome['Count'].sum()]})

         full_outcome_count = pd.concat([count_outcome, total_outcome_count], ignore_index=True)
         count_of_outcomes.set(full_outcome_count)

         total_match_played_count = full_outcome_count.loc[full_outcome_count['Match Result'] == 'Total', 'Count'].values[0]
         
         return str(total_match_played_count)
     
     @render.text
     def total_match_won():
         count_outcomes = count_of_outcomes()
         return str(count_outcomes.loc[count_outcomes['Match Result'] == 'Win', 'Count'].values[0])
     
     @render.text
     def total_match_drawed():
         count_outcomes = count_of_outcomes()
         return str(count_outcomes.loc[count_outcomes['Match Result'] == 'Draw', 'Count'].values[0])
     
     @render.text
     def total_match_lost():
         count_outcomes = count_of_outcomes()
         return str(count_outcomes.loc[count_outcomes['Match Result'] == 'Lost', 'Count'].values[0])
     
     @output
     @render.data_frame
     def barca_num_of_match_played_overall():
       barca_data_filtered = apply_filter(barca_data, match_played_place(), log)
       barca_data_filtered['Year'] = barca_data_filtered['Date'].dt.year
       temp = barca_data_filtered.groupby(['Match Result', 'Season']).size().reset_index(name='Number Of Games')
       year_data.set(temp) 
       
       return render.DataGrid(temp)

     @render_widget
     def overall_match_bar_graph():
        df = year_data.get()

        fig = plot_bar_graph_stacked(df, x_col= 'Season', y_col='Number Of Games', log=log, color_col='Match Result', color=colors.ba_sequential_color.barca_sequential_default_colors, text_col='Number Of Games')
        fig.update_layout(bargap=0.6)
        return fig
     @render_widget
     def total_played_bargraph():
         barca_data_filtered = apply_filter(barca_data, match_played_place(),log)
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

       

log.info('Rendering Overall Panel')