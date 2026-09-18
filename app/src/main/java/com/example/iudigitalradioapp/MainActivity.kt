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
 * La conexión temporal con [AudioDemoRoute] permite que Jorge Echavarría
 * pruebe Media3 ExoPlayer sin perder la cámara ya integrada por Edwin Ruiz.
 * Juan Ardila reemplazará esta conexión por RadioRoute al integrar el producto.
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
