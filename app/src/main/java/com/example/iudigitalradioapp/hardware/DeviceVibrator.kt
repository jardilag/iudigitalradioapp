package com.example.iudigitalradioapp.hardware

import android.content.Context
import android.os.VibrationEffect
import android.os.Vibrator

/**
 * Envía una confirmación háptica breve después de capturar una fotografía
 * o al pulsar los controles de reproducción. El permiso VIBRATE es de
 * instalación y se declara en AndroidManifest.xml.
 */
class DeviceVibrator(context: Context) {

    private val vibrator: Vibrator? = context.applicationContext
        .getSystemService(Vibrator::class.java)

    fun confirmPhotoCaptured() {
        vibrator?.vibrate(
            VibrationEffect.createPredefined(VibrationEffect.EFFECT_DOUBLE_CLICK)
        )
    }

    /**
     * Confirma la pulsación de Play, Pause o Mute con un clic háptico corto.
     */
    fun confirmPlaybackControlPressed() {
        vibrator?.vibrate(
            VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK)
        )
    }
}
