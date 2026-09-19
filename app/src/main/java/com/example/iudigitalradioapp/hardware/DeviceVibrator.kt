package com.example.iudigitalradioapp.hardware

import android.content.Context
import android.os.VibrationEffect
import android.os.Vibrator

/**
 * Rol responsable en la simulación: Edwin Ruiz.
 *
 * Envía una confirmación háptica breve después de capturar una fotografía. El
 * permiso VIBRATE es de instalación y se declara en AndroidManifest.xml.
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
     * Integración compartida con el módulo de Jorge Echavarría.
     * Confirma la pulsación de Play, Pause o Mute con un clic háptico corto.
     */
    fun confirmPlaybackControlPressed() {
        vibrator?.vibrate(
            VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK)
        )
    }
}
