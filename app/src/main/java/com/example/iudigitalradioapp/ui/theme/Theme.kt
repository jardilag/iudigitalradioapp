package com.example.iudigitalradioapp.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = RadioBlueLight,
    onPrimary = RadioNavy,
    secondary = RadioNavyLight,
    tertiary = RadioOrange,
    onTertiary = Color.Black,
    background = RadioDarkBackground,
    surface = RadioDarkSurface
)

private val LightColorScheme = lightColorScheme(
    primary = RadioBlue,
    onPrimary = Color.White,
    secondary = RadioNavy,
    onSecondary = Color.White,
    tertiary = RadioOrangeDark,
    background = RadioBackground,
    surface = RadioSurface,
    surfaceVariant = RadioSurfaceVariant,
    onSurface = RadioNavy
)

/** Tema visual mantenido por el rol simulado de Juan Pablo Gonzalez. */
@Suppress("UNUSED_PARAMETER")
@Composable
fun IudigitalradioappTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    // La paleta se mantiene estable para que la evidencia sea consistente.
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
