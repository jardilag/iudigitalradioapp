package com.example.iudigitalradioapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.iudigitalradioapp.hardware.HardwareDemoRoute
import com.example.iudigitalradioapp.ui.theme.IudigitalradioappTheme

/**
 * Punto de entrada de la aplicación.
 *
 * La conexión temporal con [HardwareDemoRoute] permite que Edwin Ruiz pruebe
 * la cámara, el permiso y la vibración sobre la interfaz existente. Juan
 * Ardila reemplazará esta conexión por RadioRoute en la integración final.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            IudigitalradioappTheme {
                HardwareDemoRoute()
            }
        }
    }
}
