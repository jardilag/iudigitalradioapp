package com.example.iudigitalradioapp.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Muestra los controles y emite intenciones. La reproducción y el volumen
 * reales se conectan con el módulo de audio.
 */
@Composable
fun PlaybackControls(
    hasSelectedStation: Boolean,
    isPlaying: Boolean,
    isMuted: Boolean,
    onPlayPause: () -> Unit,
    onToggleMute: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Text(
            text = "Controles",
            style = MaterialTheme.typography.titleMedium
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Button(
                onClick = onPlayPause,
                enabled = hasSelectedStation,
                modifier = Modifier.weight(1f)
            ) {
                Text(text = if (isPlaying) "Pausar" else "Reproducir")
            }
            FilledTonalButton(
                onClick = onToggleMute,
                enabled = hasSelectedStation,
                modifier = Modifier.weight(1f)
            ) {
                Text(text = if (isMuted) "Activar sonido" else "Silenciar")
            }
        }
    }
}
