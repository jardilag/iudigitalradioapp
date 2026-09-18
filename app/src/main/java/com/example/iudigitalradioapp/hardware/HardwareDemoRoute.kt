package com.example.iudigitalradioapp.hardware

import android.content.pm.PackageManager
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.RadioReducer
import com.example.iudigitalradioapp.ui.RadioScreen
import com.example.iudigitalradioapp.ui.createInitialRadioUiState

/**
 * Rol responsable en la simulación: Edwin Ruiz.
 *
 * Coordinador provisional usado para comprobar cámara, permiso y vibración.
 * Juan Ardila trasladará estos efectos a RadioRoute durante la integración.
 */
@Composable
fun HardwareDemoRoute() {
    val context = LocalContext.current
    val deviceVibrator = remember(context) {
        DeviceVibrator(context)
    }
    var state by remember {
        mutableStateOf(createInitialRadioUiState())
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

            CameraPermission.isGranted(context) -> {
                cameraLauncher.launch(null)
            }

            else -> {
                permissionLauncher.launch(CameraPermission.permission)
            }
        }
    }

    RadioScreen(
        state = state,
        onAction = { action ->
            if (action == RadioAction.OpenCamera) {
                requestCamera()
            } else {
                state = RadioReducer.reduce(state, action)
            }
        }
    )
}
