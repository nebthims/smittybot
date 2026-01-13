import subprocess
import shutil
import discord
from yt_dlp import YoutubeDL
from discord.ext import commands

class GrooTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_process = None
        print(" - GROOVY 3.0: Ready!")

    async def ensure_voice(self, ctx):
        """Ensure the bot is in the same voice channel as the author."""
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel.")
            return None

        channel = ctx.message.author.voice.channel
        voice_client = ctx.guild.voice_client
        if not voice_client:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        return voice_client

    @commands.command()
    async def play(self, ctx, url: str):
        voice_client = await self.ensure_voice(ctx)
        if not voice_client:
            return

        # Stop any existing audio stream
        if voice_client.is_playing():
            voice_client.stop()

        # Start streaming the ALSA loopback
        ffmpeg_opts = {
            "before_options": "-f alsa",
            "options": "-ac 2 -ar 48000"
        }
        audio_source = discord.FFmpegPCMAudio(
            executable="ffmpeg",
            source="hw:0,1",  # Your ALSA loopback monitor
            **ffmpeg_opts
        )
        voice_client.play(audio_source)

        # Stop previous mpv process
        if self.current_process:
            self.current_process.terminate()

        # Extract direct audio URL via yt-dlp
        ytdlp_path = shutil.which("yt-dlp")
        try:
            direct_url = subprocess.check_output(
                [ytdlp_path, "-f", "bestaudio", "-g", url],
                text=True
            ).strip()
        except subprocess.CalledProcessError:
            await ctx.send("Failed to extract audio from the YouTube URL.")
            return

        # Spawn mpv to play the extracted URL
        self.current_process = subprocess.Popen([
            "mpv",
            "--no-video",
            "--audio-device=alsa/plughw:0,0",  # Your loopback device
            direct_url
        ])

        await ctx.send(f"Joined {voice_client.channel.name} and playing YouTube audio: {url}")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect() 

        if self.current_process:
            self.current_process.terminate()
            self.current_process = None

        await ctx.send("Stopped playback and streaming.")

async def setup(bot):
    await bot.add_cog(GrooTube(bot))
