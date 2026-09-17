package com.example.iudigitalradioapp.audio

interface RadioPlayer {

    fun play(streamUrl: String)

    fun pause()

    fun setMuted(isMuted: Boolean)

    fun release()
}