package com.example.iudigitalradioapp.integration

import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import com.example.iudigitalradioapp.MainActivity
import org.junit.Rule
import org.junit.Test

/** Pruebas del producto integrado asignadas al rol simulado de Yeison Padron. */
class FinalUserFlowTest {

    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun finalScreenContainsStationsControlsAndCamera() {
        composeRule.onNodeWithText("IU Digital Radio").assertIsDisplayed()
        composeRule.onAllNodesWithText("WKDU Philadelphia 91.7 FM")
            .assertCountEquals(2)
        composeRule.onNodeWithText("KEXP").assertExists()
        composeRule.onNodeWithText("NUCROOZE Radio").assertExists()
        composeRule.onNodeWithText("Groove Salad").assertExists()
        composeRule.onNodeWithText("Indie Pop Rocks!").assertExists()
        composeRule.onNodeWithText("Reproducir").assertIsDisplayed()
        composeRule.onNodeWithText("Silenciar").assertIsDisplayed()
        composeRule.onNodeWithText("Abrir cámara")
            .performScrollTo()
            .assertIsDisplayed()
    }

    @Test
    fun selectingPlayingMutingAndPausingUpdatesTheFinalScreen() {
        composeRule.onNodeWithText("KEXP").performClick()
        composeRule.onAllNodesWithText("KEXP").assertCountEquals(2)
        composeRule.onNodeWithText("EN PAUSA").assertIsDisplayed()

        composeRule.onNodeWithText("Reproducir").performClick()
        composeRule.onNodeWithText("EN REPRODUCCIÓN").assertIsDisplayed()
        composeRule.onNodeWithText("Pausar").assertIsDisplayed()

        composeRule.onNodeWithText("Silenciar").performClick()
        composeRule.onNodeWithText("Activar sonido").assertIsDisplayed()

        composeRule.onNodeWithText("Pausar").performClick()
        composeRule.onNodeWithText("EN PAUSA").assertIsDisplayed()
        composeRule.onNodeWithText("Reproducir").assertIsDisplayed()
    }
}
