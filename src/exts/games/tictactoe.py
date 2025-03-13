import games.tictactoe as ttt
import games.discord as dgames
from discord.ext import commands
import discord
from discord import app_commands


class View(discord.ui.View):
    def __init__(self, lobby: dgames.Lobby):
        super().__init__()
        self.lobby = lobby
        self.game = ttt.TicTacToe()

        self.knots = list(lobby.joined)[0]
        self.crosses = list(lobby.joined)[1]

        self.marker_x = 0
        self.marker_y = 0

    def get_player_for_turn(self) -> int:
        if self.game.current_turn == ttt.Players.Knots:
            return self.knots
        else:
            return self.crosses

    def show_embed(self):
        if self.game.checkpoint.win_state != ttt.WinState.NoOne:
            desc = ""
            field = self.game.playfield.copy()
            field = [[a.value for a in row] for row in field]
            for i, row in enumerate(field):
                desc += "".join(row)
                desc += "\n"

            embed = discord.Embed(
                title=self.game.checkpoint.win_state.value,
                description=desc,
                color=discord.Color.red(),
            )

            return embed

        desc = ""
        field = self.game.playfield.copy()
        field = [[a.value for a in row] for row in field]

        if self.game.current_turn == ttt.Players.Knots:
            marker = "🅾️"
        else:
            marker = "❎"

        field[self.marker_y][self.marker_x] = marker
        for i, row in enumerate(field):
            desc += "".join(row)
            desc += "\n"
        title = f"Its {self.game.current_turn.value}'s turn"

        embed = discord.Embed(title=title, description=desc, color=discord.Color.red())

        return embed

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id not in list(self.lobby.joined):
            await interaction.response.send_message(
                content="You are not in this game!", ephemeral=True
            )
            return False

        if interaction.user.id != self.get_player_for_turn():
            await interaction.response.send_message(
                content="Wait your turn!", ephemeral=True
            )
            return False

        return True

    @discord.ui.button(emoji="⬅️")
    async def go_left(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.marker_x -= 1

        if self.marker_x == -1:
            self.marker_x = self.game.size - 1

        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="➡️")
    async def go_right(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.marker_x += 1

        if self.marker_x == self.game.size:
            self.marker_x = 0

        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="⬆️")
    async def go_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.marker_y -= 1

        if self.marker_y == -1:
            self.marker_y = self.game.size - 1

        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="⬇️")
    async def go_down(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.marker_y += 1

        if self.marker_y == self.game.size:
            self.marker_y = 0

        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="✅")
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            checkpoint = self.game.play_move(self.marker_x, self.marker_y)
            if checkpoint.win_state != ttt.WinState.NoOne:
                await interaction.response.edit_message(
                    embed=self.show_embed(), view=None
                )
                return
            await interaction.response.edit_message(embed=self.show_embed(), view=self)
        except ValueError as e:
            await interaction.response.send_message(content=str(e), ephemeral=True)


class Lobby(dgames.LobbyView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_play = "Tic Tac Toe"

    async def on_start(self, interaction: discord.Interaction, lobby: dgames.Lobby):
        view = View(lobby)
        await interaction.channel.send(embed=view.show_embed(), view=view)


class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="tictactoe", description="Play a game of Tic Tac Toe!")
    async def tictactoe(self, interaction: discord.Interaction):
        # logger.debug("New tictactoe game started!")
        view = Lobby(min_players=2)
        await interaction.response.send_message(embed=view.make_embed(), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(TicTacToe(bot))
