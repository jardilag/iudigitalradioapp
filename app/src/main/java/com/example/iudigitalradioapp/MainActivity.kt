package com.example.iudigitalradioapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.iudigitalradioapp.audio.AudioDemoRoute
import com.example.iudigitalradioapp.ui.theme.IudigitalradioappTheme

/**
 * Punto de entrada de la aplicación.
 *
 * La conexión temporal con [AudioDemoRoute] permite probar Media3 ExoPlayer
 * sin perder la cámara ya integrada.
 * RadioRoute reemplazará esta conexión al integrar el producto.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            IudigitalradioappTheme {
                AudioDemoRoute()
            }
        }
    }
}
