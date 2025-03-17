import discord


class Lobby:
    def __init__(self, min_players: int, max_players: int):
        self.min_players: int = min_players
        self.max_players: int = max_players
        self.joined: set[int] = set()  # Store IDs instead of objects

    def join(self, user: discord.User):
        if len(self.joined) == self.max_players:
            return

        self.joined.add(user.id)  # Store the user ID

    def leave(self, user: discord.User):
        self.joined.remove(user.id)


class LobbyView(discord.ui.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.lobby = Lobby(*args, **kwargs)
        self.to_play = "Some Unknown Game"

    def make_embed(self) -> discord.Embed:
        desc = "\n".join([f"<@{user_id}>" for user_id in list(self.lobby.joined)])
        desc += f"\n\nMinimum Players: {self.lobby.min_players} | Maximum Players: {self.lobby.max_players} | Current players: {len(self.lobby.joined)}"
        return discord.Embed(
            title=self.to_play, description=desc, color=discord.Color.gold()
        )

    @discord.ui.button(label="Join", emoji="👋")
    async def join_lobby(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.lobby.join(interaction.user)
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="Leave", emoji="🏃")
    async def leave_lobby(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.lobby.leave(interaction.user)
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @discord.ui.button(label="Start", emoji="🎮")
    async def start_lobbys_game(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if len(self.lobby.joined) < self.lobby.min_players:
            await interaction.response.send_message(
                content="There are too little people in the lobby!", ephemeral=True
            )
            return

        await interaction.message.delete()
        await self.on_start(interaction, self.lobby)

    @discord.ui.button(label="Close", emoji="❌")
    async def close_lobby(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.message.delete()

    # to be overriden
    async def on_start(self, interaction: discord.Interaction, lobby: Lobby) -> None:
        pass
