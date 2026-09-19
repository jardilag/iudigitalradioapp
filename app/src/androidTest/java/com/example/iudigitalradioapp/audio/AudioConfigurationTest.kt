package com.example.iudigitalradioapp.audio

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

/** Prueba instrumentada de configuración del rol simulado de Jorge Echavarría. */
@RunWith(AndroidJUnit4::class)
class AudioConfigurationTest {

    @Test
    fun manifestDeclaresInternetPermission() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val packageInfo = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            context.packageManager.getPackageInfo(
                context.packageName,
                PackageManager.PackageInfoFlags.of(PackageManager.GET_PERMISSIONS.toLong())
            )
        } else {
            @Suppress("DEPRECATION")
            context.packageManager.getPackageInfo(
                context.packageName,
                PackageManager.GET_PERMISSIONS
            )
        }

        assertTrue(
            Manifest.permission.INTERNET in packageInfo.requestedPermissions.orEmpty()
        )
    }
}
