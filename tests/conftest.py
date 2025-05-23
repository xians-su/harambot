import os
import json
import pytest

from unittest.mock import MagicMock, patch
from harambot.yahoo_api import Yahoo
from yahoo_fantasy_api import game, League, Team

root_path = os.path.dirname(os.path.realpath(__file__))


def load_test_data(filename):
    with open(root_path + "/" + filename, "r") as f:
        test_data = json.load(f)
        f.close()
    return test_data


@pytest.fixture
def mock_oauth():
    oauth = MagicMock()
    oauth.token_is_valid.return_value = True
    return oauth


@pytest.fixture
def mock_standings():
    return load_test_data("test-standings.json")["standings"]


@pytest.fixture
def mock_teams():
    return load_test_data("test-teams.json")


@pytest.fixture
def mock_roster():
    return load_test_data("test-roster.json")["roster"]


@pytest.fixture
def mock_player_details():
    return load_test_data("test-player-details.json")["details"]


@pytest.fixture
def mock_player_stats():
    return [
        {
            "mock": "stats",
            "player_id": "39077",
            "name": "Josh Allen",
            "position_type": "o",
        }
    ]


@pytest.fixture
def mock_ownership():
    return load_test_data("test-player-details.json")["ownership"]


@pytest.fixture
def mock_matchups():
    return load_test_data("test-matchups.json")


@pytest.fixture
def mock_matchups_category():
    return load_test_data("test-matchups-category.json")

@pytest.fixture
def mock_pending_trades():
    raw_pending_trade_data = load_test_data("test-pending-trade.json")
    return [raw_pending_trade_data["fantasy_content"]["transaction"]]


@pytest.fixture
def mock_league_settings():
    return load_test_data("test-league-settings.json")["settings"]



@pytest.fixture
def api(
    mock_oauth,
    mock_standings,
    mock_teams,
    mock_player_details,
    mock_player_stats,
    mock_ownership,
    mock_matchups,
    mock_pending_trades,
    
):
    api = Yahoo()
    api.scoring_type = "head"
    league = None
    with patch.object(game.Game, "game_id", return_value="319"):
        # mock the settings() method of League class
        # to return a dictionary with the game_code key
        # and a value of "114"
        with patch.object(League, "settings", return_value={"game_code": "114"}):
            with patch.object(League, "_cache_stats_id_map", return_value=None):
                league = League(mock_oauth, 123456)
                team = Team(mock_oauth, "")
                team.proposed_trades = MagicMock(return_value=mock_pending_trades)
                league.standings = MagicMock(return_value=mock_standings)
                league.teams = MagicMock(return_value=mock_teams)
                league.current_week = MagicMock(return_value=1)
                league.player_details = MagicMock(return_value=mock_player_details)
                league.player_stats = MagicMock(return_value=mock_player_stats)
                league.ownership = MagicMock(return_value=mock_ownership)
                league.matchups = MagicMock(return_value=mock_matchups)
                league.get_team = MagicMock(
                    return_value={"Too Many Cooks": team}
                )
                league.to_team = MagicMock(
                        return_value=team
                )
    
    api.league = MagicMock(return_value=league)
    return api


@pytest.fixture
def category_api(
    mock_oauth,
    mock_standings,
    mock_teams,
    mock_player_details,
    mock_player_stats,
    mock_ownership,
    mock_matchups_category,
):
    api = Yahoo()
    api.scoring_type = "headone"
    league = None
    with patch.object(game.Game, "game_id", return_value="319"):
        with patch.object(League, "settings", return_value={"game_code": "114"}):
            with patch.object(League, "_cache_stats_id_map", return_value=None):
                league = League(mock_oauth, 123456)
                league.standings = MagicMock(return_value=mock_standings)
                league.teams = MagicMock(return_value=mock_teams)
                league.current_week = MagicMock(return_value=1)
                league.player_details = MagicMock(return_value=mock_player_details)
                league.player_stats = MagicMock(return_value=mock_player_stats)
                league.ownership = MagicMock(return_value=mock_ownership)
                league.matchups = MagicMock(return_value=mock_matchups_category)
    api.league = MagicMock(return_value=league)
    return api
