from bs4 import BeautifulSoup
import pandas as pd
import requests

class MakeEventDataset:

    def __init__(self, link):
        self.link = link

    def get_event_info(self, timeline, minutes, side):
        """
        Function to scrape the event timeline.

        Arguments
        ---------
          timeline : bs4.element.ResultSet
            The HTML code inside a list for events
          minutes : bs4.element.ResultSet
            The HTML code inside a list for minutes
          side : str
            Either H or A

        Returns
        -------
        list : containing all the events as dictionary
        """

        # init an empty list
        dataframe_list = []

        for events, time in zip(timeline, minutes):
            for event in events.find_all("div", {"class": "timeline-row"}):
                # fetch player names
                player_names = event.find_all("a", {"class": "player-name"})

                # fetch shape detail
                shape_detail = event.i["title"]

                # if there are more than one player name then it's a substituition
                if len(player_names) > 1:
                    player_name = player_names[0].get_text()
                    event_detail = player_names[1].get_text()
                else:
                    player_name = player_names[0].get_text()

                    if event.span is None:
                        event_detail = ''
                    else:
                        event_detail = event.span.get_text()

                # fetch minute
                minute = int(time.span.get_text()[:-1])

                # add to the list
                dataframe_list.append({
                    "Name": player_name,
                    "Shape Detail": shape_detail,
                    "Event Detail": event_detail,
                    "Minute": minute,
                    "H_A": side,
                })

        return dataframe_list

    def get_event_df(self):
        # scrape HTML from the given link
        page_tree = requests.get(self.link)
        page_soup = BeautifulSoup(page_tree.content, "html.parser")

        # fetch home-events
        timeline_home = page_soup.find_all("div", {"class": "timeline-block block-home"})

        # fetch away-events
        timeline_away = page_soup.find_all("div", {"class": "timeline-block block-away"})

        # fetch time
        minutes = page_soup.find_all("div", {"class": "timeline-minute"})

        # get dataframe list for both home and away teams
        dataframe_list_home = self.get_event_info(timeline_home, minutes, 'H')
        dataframe_list_away = self.get_event_info(timeline_away, minutes, 'A')

        # make final dataframe list
        final_df_list = [*dataframe_list_home, *dataframe_list_away]

        # make final dataframe
        event_df = pd.DataFrame(final_df_list).sort_values(
            by="Minute"
        ).reset_index(
            drop=True
        )

        return event_df

obj = MakeEventDataset("https://understat.com/match/16432")
event_df = obj.get_event_df()

# save in csv format
event_df.to_csv("event_file.csv", index=False)
