package com.example.iudigitalradioapp.ui

import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.example.iudigitalradioapp.MainActivity
import org.junit.Rule
import org.junit.Test

/** Pruebas de interfaz del rol simulado de Juan Pablo Gonzalez. */
class RadioScreenTest {

    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun selectedStationAndControlsAreVisible() {
        composeRule.onNodeWithText("Radio universitaria - Drexel University").assertIsDisplayed()
        composeRule.onNodeWithText("Reproducir").assertIsDisplayed()
        composeRule.onNodeWithText("Abrir cámara").assertExists()
    }

    @Test
    fun allFiveStationsAreVisibleWithoutHorizontalScroll() {
        composeRule.onAllNodesWithText("WKDU Philadelphia 91.7 FM")
            .assertCountEquals(2)[0]
            .assertIsDisplayed()

        listOf(
            "KEXP",
            "NUCROOZE Radio",
            "Groove Salad",
            "Indie Pop Rocks!"
        ).forEach { stationName ->
            composeRule.onNodeWithText(stationName).assertIsDisplayed()
        }
    }

    @Test
    fun playButtonUpdatesVisibleState() {
        composeRule.onNodeWithText("Reproducir").performClick()

        composeRule.onNodeWithText("Pausar").assertIsDisplayed()
        composeRule.onNodeWithText("EN REPRODUCCIÓN").assertIsDisplayed()
    }
}
