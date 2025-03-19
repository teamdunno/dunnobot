import games.connect4 as c4
import games.discord as dgames
from discord.ext import commands
import discord
from discord import app_commands


class View(discord.ui.View):
    def __init__(self, lobby: dgames.Lobby):
        super().__init__()
        self.lobby = lobby
        self.game = c4.Connect4(player_count=len(lobby.joined))
        self.players = list(lobby.joined)
        self.current_column = 0

    def get_player_for_turn(self) -> int:
        return self.players[self.game.current_turn_idx]

    def show_embed(self):
        if self.game.checkpoint.win_state != c4.WinState.NoOne:
            desc = ""
            field = [[a.value for a in row] for row in self.game.playfield]
            for row in field:
                desc += "".join(row) + "\n"

            embed = discord.Embed(
                title=self.game.checkpoint.win_state.value,
                description=desc,
                color=discord.Color.red(),
            )
            return embed

        desc = ""
        field = [[a.value for a in row] for row in self.game.playfield]
        marker_row = [
            "⬇️" if i == self.current_column else "⚫" for i in range(self.game.width)
        ]
        field.insert(0, marker_row)

        for row in field:
            desc += "".join(row) + "\n"

        title = f"It's {self.game.players[self.game.current_turn_idx].value}'s turn"
        embed = discord.Embed(title=title, description=desc, color=discord.Color.red())
        return embed

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id not in self.players:
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
        self.current_column = (self.current_column - 1) % self.game.width
        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="➡️")
    async def go_right(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.current_column = (self.current_column + 1) % self.game.width
        await interaction.response.edit_message(embed=self.show_embed(), view=self)

    @discord.ui.button(emoji="✅")
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            checkpoint = self.game.play_move(self.current_column)
            if checkpoint.win_state != c4.WinState.NoOne:
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
        self.to_play = "Connect 4"

    async def on_start(self, interaction: discord.Interaction, lobby: dgames.Lobby):
        view = View(lobby)
        await interaction.channel.send(embed=view.show_embed(), view=view)


class Connect4(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="connectfour", description="Play a game of Connect 4!")
    async def connect4(self, interaction: discord.Interaction):
        view = Lobby(min_players=2, max_players=4)
        await interaction.response.send_message(embed=view.make_embed(), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Connect4(bot))
