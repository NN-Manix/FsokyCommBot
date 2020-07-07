# Импорт
import discord
import config
from discord.ext import commands


# Код
class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Модераторские"]

    @commands.command(
        aliases=["клеар", "clr", "cls", "очистить", "очст"],
        description="Это сообщение",
        usage="clear [количество сообщений для удаления]")
    @commands.has_permissions( manage_messages = True)
    async def clear( ctx, amount: int ):
        if not amount:
              await ctx.send("Пожалуйста, используйте такую кострукцию: `!!clear [количество сообщений для удаления]`")
              return
        await ctx.channel.purge( limit =  (amount + 1) )

        await ctx.sent(f"Удалено {amount} сообщений")

    @commands.command()
	@commands.has_permissions( administrator = True )
	async def vmute( self, ctx, member: discord.Member, vmute_time: int = 0 ):
		client = self.bot
		guild = ctx.guild
		vmute_minutes = vmute_time * 60
		overwrite = discord.PermissionOverwrite( connect = False )
		role = get( ctx.guild.roles, name = "Vmute_role" )

		if role == None:
			role = await guild.create_role( name = "Vmute_role" )

		for channel in guild.voice_channels:
			await channel.set_permissions( role, overwrite = overwrite )

		await member.add_roles( role )
		await member.edit( voice_channel = None )

		if vmute_minutes > 0:
			emb = discord.Embed( description = f'**{ctx.message.author.mention} Замутил {member.mention} в голосовых каналах на {vmute_time}мин**' , colour = discord.Color.green() )			
			emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
			emb.set_footer( text = Footer, icon_url = client.user.avatar_url )			
			await ctx.send( embed = emb )

			await asyncio.sleep(vmute_minutes)
			await member.remove_roles( role )

			overwrite = discord.PermissionOverwrite( connect = None )
			for channel in guild.voice_channels:
				await channel.set_permissions( role, overwrite = overwrite )
		elif vmute_minutes <= 0:
			emb = discord.Embed( description = f'**{ctx.message.author.mention} Перманентно замутил {member.mention} в голосовых каналах**' , colour = discord.Color.green() )			
			emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
			emb.set_footer( text = Footer, icon_url = client.user.avatar_url )			
			await ctx.send( embed = emb )
            
 	@commands.command(aliases = ['un-vmute'])
	@commands.has_permissions( administrator = True )
	async def unvmute( self, ctx, member: discord.Member ):
		client = self.bot
		guild = ctx.guild

		for vmute_role in guild.roles:
			if vmute_role.name == Vmute_role:
				await member.remove_roles( vmute_role )

				overwrite = discord.PermissionOverwrite( connect = None )

				for channel in guild.voice_channels:
					await channel.set_permissions( vmute_role, overwrite = overwrite )

				emb = discord.Embed( description = f'**{ctx.message.author.mention} Размутил {member.mention} в голосовых каналах**' , colour = discord.Color.green() )				
				emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
				emb.set_footer( text = Footer, icon_url = client.user.avatar_url )		
				await ctx.send( embed = emb )
				return

def setup(client):
    client.add_cog(Moder(client))
