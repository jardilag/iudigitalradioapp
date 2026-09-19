package com.example.iudigitalradioapp.hardware

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat

/**
 * Centraliza el nombre y la consulta del permiso de cámara. La solicitud se
 * realiza desde la ruta de la pantalla porque necesita un lanzador de actividad.
 */
object CameraPermission {

    const val permission: String = Manifest.permission.CAMERA

    fun isGranted(context: Context): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            permission
        ) == PackageManager.PERMISSION_GRANTED
    }
}
