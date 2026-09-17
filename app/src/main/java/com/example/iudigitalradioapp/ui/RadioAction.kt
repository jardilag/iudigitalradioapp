package com.example.iudigitalradioapp.ui

import android.graphics.Bitmap

sealed interface RadioAction {

    data object Play : RadioAction

    data object Pause : RadioAction

    data object ToggleMute : RadioAction

    data object OpenCamera : RadioAction

    data class SelectStation(
        val stationId: String
    ) : RadioAction

    data class PhotoCaptured(
        val bitmap: Bitmap
    ) : RadioAction
}