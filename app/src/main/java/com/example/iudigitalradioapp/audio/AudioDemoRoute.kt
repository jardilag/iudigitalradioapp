package com.example.iudigitalradioapp.audio

import android.content.pm.PackageManager
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import com.example.iudigitalradioapp.hardware.CameraPermission
import com.example.iudigitalradioapp.hardware.DeviceVibrator
import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.RadioReducer
import com.example.iudigitalradioapp.ui.RadioScreen
import com.example.iudigitalradioapp.ui.createInitialRadioUiState

/**
 * Coordinador provisional para probar el audio real de esta rama. Reutiliza
 * el flujo de cámara para no perder una función ya validada.
 * RadioRoute reemplazará esta conexión durante la integración.
 */
@Composable
fun AudioDemoRoute() {
    val context = LocalContext.current
    val deviceVibrator = remember(context) {
        DeviceVibrator(context)
    }
    val radioPlayer = remember(context) {
        Media3RadioPlayer(context) { message ->
            Toast.makeText(context, message, Toast.LENGTH_LONG).show()
        }
    }
    val audioActionHandler = remember(radioPlayer) {
        AudioActionHandler(radioPlayer)
    }
    var state by remember {
        mutableStateOf(createInitialRadioUiState())
    }

    DisposableEffect(radioPlayer) {
        onDispose {
            radioPlayer.release()
        }
    }

    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap == null) {
            Toast.makeText(
                context,
                "La captura fue cancelada.",
                Toast.LENGTH_SHORT
            ).show()
        } else {
            state = RadioReducer.reduce(
                state = state,
                action = RadioAction.PhotoCaptured(bitmap)
            )
            deviceVibrator.confirmPhotoCaptured()
        }
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            cameraLauncher.launch(null)
        } else {
            Toast.makeText(
                context,
                "El permiso de cámara es necesario para tomar la fotografía.",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    fun requestCamera() {
        val hasCamera = context.packageManager.hasSystemFeature(
            PackageManager.FEATURE_CAMERA_ANY
        )

        when {
            !hasCamera -> {
                Toast.makeText(
                    context,
                    "Este dispositivo no tiene una cámara disponible.",
                    Toast.LENGTH_LONG
                ).show()
            }

            CameraPermission.isGranted(context) -> cameraLauncher.launch(null)

            else -> permissionLauncher.launch(CameraPermission.permission)
        }
    }

    RadioScreen(
        state = state,
        onAction = { action ->
            when (action) {
                RadioAction.OpenCamera -> requestCamera()

                RadioAction.Play,
                RadioAction.Pause,
                RadioAction.ToggleMute -> {
                    deviceVibrator.confirmPlaybackControlPressed()
                    state = audioActionHandler.handle(state, action)
                }

                else -> {
                    state = audioActionHandler.handle(state, action)
                }
            }
        }
    )
}
