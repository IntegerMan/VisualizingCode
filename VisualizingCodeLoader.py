import pandas as pd



def load_and_clean_release_data(path):
    # Load release data
    df_releases = pd.read_csv(path, sep='\t', names=['ID','Tag','Name','Date'],parse_dates=['Date'])

    # Ensure our releases are tagged as releases instead of NA
    df_releases['Tag'] = df_releases['Tag'].fillna('Release')

    # Instead of Latest, use Release for the latest release. This will help us compare releases
    df_releases['Tag'] = df_releases['Tag'].replace(['Latest'], 'Release')

    return df_releases

    
def load_and_clean_issue_data(path):
    # Load issue data
    df_issues = pd.read_csv(path, sep='\t', names=['ID', 'Status', 'Message', 'Labels', 'Date'])

    # Ensure the Date column can be worked with as a date later on. Sample date format: 2021-12-28 11:42:22 +0000 UTC
    df_issues['Date'] = pd.to_datetime(df_issues['Date'], utc=True, format='%Y-%m-%d %H:%M:%S %z UTC')

    # Ensure our labels use empty strings instead of NA
    df_issues['Labels'] = df_issues['Labels'].fillna('')

    # Feature Engineering - Add in explicit columns for various pieces of information present in the labels
    df_issues['Is Bug'] = df_issues['Labels'].str.contains('Bug|Crash|Performance|Regression|Limitation', case=False)
    df_issues['Is Support'] = df_issues['Labels'].str.contains('Question / Support', case=False)
    df_issues['Is Feature'] = df_issues['Labels'].str.contains('Feature|Polish|Idea/Wishlist', case=False)
    df_issues['Is Overhead'] = df_issues['Labels'].str.contains('Refactor|Documentation|Packaging', case=False)
    df_issues['Is AI'] = df_issues['Labels'].str.contains('AI', case=False)
    df_issues['Is Networking'] = df_issues['Labels'].str.contains('Networking', case=False)
    df_issues['Is Mod'] = df_issues['Labels'].str.contains('Mod Support|Scripting', case=False)
    df_issues['Is Dune'] = df_issues['Labels'].str.contains('Dune 2000', case=False)
    df_issues['Is Red Alert'] = df_issues['Labels'].str.contains('Red Alert', case=False)
    df_issues['Is Tiberian Sun'] = df_issues['Labels'].str.contains('Tiberian Sun', case=False)
    df_issues['Is Tiberian Dawn'] = df_issues['Labels'].str.contains('Tiberian Dawn', case=False)
    df_issues['Is Closed'] = df_issues['Status'] == 'CLOSED'

    # Charting the # Closed and # Open as numbers here makes aggregation far easier. These are just going to be 0 and 1 here, but in aggregate it's easier to total things up
    df_issues['# Closed'] = df_issues['Is Closed'] * 1
    df_issues['# Open'] = 1 - df_issues['# Closed']

    # This function will be applied to every row
    def assign_issue_features(row):
        if row['Is Red Alert']:
            row['Game'] = 'Red Alert'
        elif row['Is Tiberian Sun']:
            row['Game'] = 'Tiberian Sun'
        elif row['Is Tiberian Dawn']:
            row['Game'] = 'Tiberian Dawn'
        elif row['Is Dune']:
            row['Game'] = 'Dune 2000'
        else:
            row['Game'] = 'N/A'

        if row['Is AI']:
            row['Area'] = 'AI'
        elif row['Is Networking']:
            row['Area'] = 'Networking'
        elif row['Is Mod']:
            row['Area'] = 'Mod Support'
        else:
            row['Area'] = 'Other'

        if row['Is Support']:
            row['Type'] = 'Support'
        elif row['Is Overhead']:
            row['Type'] = 'Overhead'
        elif row['Is Feature']:
            row['Type'] = 'Feature'
        else: # Most of the issue data appeared to be bugs if not explicitly labeled as not a bug, so use bug as the default
            row['Type'] = 'Bug'

        return row

    df_issues = df_issues.apply(assign_issue_features, axis=1)

    # Engineer Date Columns
    df_issues['datetime'] = pd.to_datetime(df_issues['Date'], errors='coerce', utc=True)
    df_issues['Date'] = df_issues['datetime'].dt.date
    df_issues['year'] = df_issues['datetime'].dt.year
    df_issues['month'] = df_issues['datetime'].dt.month
    df_issues['year-month'] = df_issues['datetime'].to_numpy().astype('datetime64[M]')
    df_issues['weekday'] = df_issues['datetime'].dt.weekday
    df_issues['weekday_name'] = df_issues['datetime'].dt.strftime("%A")

    # Ensure we're loaded chronologically
    df_issues = df_issues.sort_values('Date')    

    return df_issues


def load_and_clean_commit_data(path):
    df_commits = pd.read_csv(path, parse_dates=['author_date'])

    # Remove junk columns
    df_commits.drop('Unnamed: 0', axis=1, inplace=True)
    df_commits.drop('author_email', axis=1, inplace=True)
    df_commits.drop('author_tz', axis=1, inplace=True)
    df_commits.drop('committer_name', axis=1, inplace=True)
    df_commits.drop('committer_email', axis=1, inplace=True)
    df_commits.drop('committer_date', axis=1, inplace=True)
    df_commits.drop('committer_tz', axis=1, inplace=True)
    df_commits.drop('in_main', axis=1, inplace=True)
    df_commits.drop('is_merge', axis=1, inplace=True)
    df_commits.drop('branches', axis=1, inplace=True)

    # Engineer Date Columns
    df_commits['datetime'] = pd.to_datetime(df_commits['author_date'], errors='coerce', utc=True)
    df_commits['date'] = df_commits['datetime'].dt.date
    df_commits['year'] = df_commits['datetime'].dt.year
    df_commits['month'] = df_commits['datetime'].dt.month
    df_commits['year-month'] = df_commits['datetime'].to_numpy().astype('datetime64[M]')
    df_commits['weekday'] = df_commits['datetime'].dt.weekday
    df_commits['weekday_name'] = df_commits['datetime'].dt.strftime("%A")

    # We no longer need the raw author_date column
    df_commits.drop('author_date', axis=1, inplace=True)    

    # Sorting by date is important for us
    df_commits = df_commits.sort_values('date')

    return df_commits


def load_and_clean_file_data(path):
    df_files = pd.read_csv(path)

    # Remove the unwanted column
    df_files.drop('Unnamed: 0', axis=1, inplace=True)

    # This is a function we'll apply to each row of our DataFrame
    def fix_file_path(row):
        if row['path'] == '.':
            row['fullpath'] = row['project'] + '\\' + row['filename']
        else:
            row['fullpath'] = row['project'] + '\\' + row['path'] + '\\' + row['filename']
        return row

    # Apply the function to each row and update the DataFrame with the result
    df_files = df_files.apply(fix_file_path, axis=1)

    return df_files


def load_and_clean_file_commit_data(path, clean_contributors):

    df_file_commits = pd.read_csv(path)

    # Do our standard contributor cleaning
    df_file_commits = clean_contributors(df_file_commits)

    # Store the path under the fullpath column. This will make merging easier later
    df_file_commits['fullpath'] = df_file_commits['new_path']

    # Data Cleaning - Drop columns we don't care about
    df_file_commits.drop('Unnamed: 0', axis=1, inplace=True)
    df_file_commits.drop('project_name', axis=1, inplace=True)
    df_file_commits.drop('project_path', axis=1, inplace=True)
    df_file_commits.drop('new_path', axis=1, inplace=True)
    df_file_commits.drop('old_path', axis=1, inplace=True)
    df_file_commits.drop('branches', axis=1, inplace=True)
    df_file_commits.drop('in_main', axis=1, inplace=True)
    df_file_commits.drop('is_merge', axis=1, inplace=True)

    # This list is really rudimentary, but should let us guess if something is a bug or feature
    bug_indicators = ['bug', 'fix', 'issue', 'crash', 'error', 'broke', 'break', 'catastrophic', 'critical', 'urgent', 'unable']

    # Let's determine if a commit relates to a bug or a feature
    def set_is_bug(row):
        message = row['message'].lower()
        
        if bool([ele for ele in bug_indicators if(ele in message)]):
            row['is_bug'] = 1
        else:
            row['is_bug'] = 0

        return row

    df_file_commits = df_file_commits.apply(set_is_bug, axis=1)

    return df_file_commits