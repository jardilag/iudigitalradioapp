package com.example.iudigitalradioapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.iudigitalradioapp.ui.RadioScreenDemo
import com.example.iudigitalradioapp.ui.theme.IudigitalradioappTheme

/**
 * Punto de entrada de la aplicación.
 *
 * La conexión con [RadioScreenDemo] permite revisar localmente la interfaz
 * creada por el rol simulado de Juan Pablo Gonzalez. Juan Ardila reemplazará
 * esta conexión provisional por RadioRoute durante la integración final.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            IudigitalradioappTheme {
                RadioScreenDemo()
            }
        }
    }
}
