package com.example.iudigitalradioapp.audio

import android.content.Context
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer

/**
 * Implementación real de [RadioPlayer] con Media3 ExoPlayer. La clase evita
 * que Compose conozca los detalles de MediaItem, preparación, volumen o
 * liberación del reproductor.
 */
class Media3RadioPlayer(
    context: Context,
    private val onPlaybackError: (String) -> Unit = {}
) : RadioPlayer {

    private val player: ExoPlayer = ExoPlayer.Builder(
        context.applicationContext
    ).build()

    private var loadedStreamUrl: String? = null

    init {
        player.addListener(
            object : Player.Listener {
                override fun onPlayerError(error: PlaybackException) {
                    onPlaybackError(
                        error.localizedMessage ?: "No fue posible reproducir la emisora."
                    )
                }
            }
        )
    }

    override fun play(streamUrl: String) {
        if (streamUrl.isBlank()) {
            onPlaybackError("La emisora seleccionada no tiene una fuente de audio.")
            return
        }

        if (loadedStreamUrl != streamUrl) {
            player.setMediaItem(MediaItem.fromUri(streamUrl))
            player.prepare()
            loadedStreamUrl = streamUrl
        }

        player.play()
    }

    override fun pause() {
        player.pause()
    }

    override fun setMuted(isMuted: Boolean) {
        player.volume = if (isMuted) 0f else 1f
    }

    override fun release() {
        player.release()
        loadedStreamUrl = null
    }
}
