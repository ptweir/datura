import datura
import pandas as pd

sql_query = """
--sql
WITH final_score_CTE AS (
SELECT
    MIN(homeFinalRuns) AS home_runs
  , MIN(awayFinalRuns) AS away_runs
  , MIN(startTime) AS start_time
  , gameID
FROM `bigquery-public-data.baseball.games_wide`
WHERE gameStatus = 'closed'
GROUP BY gameID
)
SELECT
  AVG(home_runs) AS avg_home_runs
  , STDDEV_SAMP(home_runs) AS std_home_runs
  , AVG(away_runs) AS avg_away_runs
  , STDDEV_SAMP(away_runs) AS std_away_runs
  , COUNT( DISTINCT gameID) AS games
  , DATE_TRUNC(start_time, MONTH) AS game_month
FROM final_score_CTE
GROUP BY game_month
ORDER BY game_month
;
"""

results_df = pd.read_csv('examples/runs.csv', parse_dates=['game_month'])
results_df['sem_home'] = results_df['std_home_runs'] / results_df['games']**.5
results_df['sem_away'] = results_df['std_away_runs'] / results_df['games']**.5

datura.error_plot(results_df['game_month'],
                  results_df[['avg_home_runs', 'avg_away_runs']],
                  y_errors=results_df[['sem_home', 'sem_away']],
                  filename='examples/error_patch_example.svg',
                  x_label='Game month', y_label='Runs (+/- SE)',
                  title='Error Patch Example', labels=['Home', 'Away'],
                  label_nudges=[0, 0],
                  y_ticks=[0, 2, 4, 6])
