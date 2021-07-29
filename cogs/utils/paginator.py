from datetime import datetime
from typing import List
import discord


class Select(discord.ui.Select['Paginator']):

	def __init__(self, options: List[discord.SelectOption]) -> None:
		super().__init__(placeholder="Jump to page...", min_values=1, max_values=1, options=options, row=1)

	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		await self.view.process_callback(self, interaction)

class Paginator(discord.ui.View):

	children: List[discord.ui.Button]

	def __init__(self, ctx ,embeds: List[discord.Embed]):
		super().__init__(timeout=300.0)
		self.ctx = ctx
		self.embeds: List[discord.Embed] = embeds
		self.embed_pos = 0
		self.max = len(embeds)

		for i, embed in enumerate(self.embeds):
			embed.set_footer(text=f"{i + 1}/{self.max}")
			embed.timestamp = datetime.utcnow()

		select_options = [discord.SelectOption(label=f"{i+1}", value=str(i)) for i in range(self.max)]
		if self.max < 25:
			self.add_item(Select(select_options))
		# Well due to this we can't have more than 25 pages, so fuck selects


	async def on_timeout(self) -> None:
		return await super().on_timeout()

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		assert interaction.user is not None
		return interaction.user.id == self.ctx.author.id

	@discord.ui.button(emoji="\U000023ee", style=discord.ButtonStyle.primary)
	async def forward_start(self, button: discord.ui.Button, interaction: discord.Interaction):
		self.embed_pos = 0
		await interaction.response.edit_message(embed=self.embeds[0])

	
	@discord.ui.button(emoji="\U000023ea", style=discord.ButtonStyle.primary)
	async def backward_next(self, button: discord.ui.Button, interaction: discord.Interaction):
		if self.embed_pos - 1 < 0:
			return await interaction.response.send_message("uh- that's the first page.", ephemeral=True)
		self.embed_pos -= 1
		await interaction.response.edit_message(embed=self.embeds[self.embed_pos])

	@discord.ui.button(emoji="\U000023f9", style=discord.ButtonStyle.primary)
	async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
		for button in self.children:
			button.disabled = True
		await interaction.message.delete()
		self.stop()

	@discord.ui.button(emoji="\U000023e9", style=discord.ButtonStyle.primary)
	async def forward_next(self, button: discord.ui.Button, interaction: discord.Interaction):
		if self.embed_pos + 1 >= self.max:
			return await interaction.response.send_message("That's actually the last page lol.", ephemeral=True)
		self.embed_pos += 1
		await interaction.response.edit_message(embed=self.embeds[self.embed_pos])

	@discord.ui.button(emoji="\U000023ed", style=discord.ButtonStyle.primary)
	async def backward_end(self, button: discord.ui.Button, interaction: discord.Interaction):
		self.embed_pos = self.max - 1
		await interaction.response.edit_message(embed=self.embeds[self.embed_pos])

	async def process_callback(self,select: discord.ui.Select, interaction: discord.Interaction):
		assert interaction.data is not None
		opt: int = int(interaction.data["values"][0]) #type: ignore
		await interaction.response.edit_message(embed=self.embeds[opt])