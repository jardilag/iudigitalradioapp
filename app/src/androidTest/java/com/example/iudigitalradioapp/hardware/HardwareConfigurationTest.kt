package com.example.iudigitalradioapp.hardware

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Build
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.RadioReducer
import com.example.iudigitalradioapp.ui.createInitialRadioUiState
import org.junit.Assert.assertSame
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

/** Pruebas instrumentadas del rol simulado de Edwin Ruiz. */
@RunWith(AndroidJUnit4::class)
class HardwareConfigurationTest {

    @Test
    fun manifestDeclaresCameraAndVibrationPermissions() {
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
        val permissions = packageInfo.requestedPermissions.orEmpty().toSet()

        assertTrue(Manifest.permission.CAMERA in permissions)
        assertTrue(Manifest.permission.VIBRATE in permissions)
    }

    @Test
    fun capturedPhotoIsStoredInScreenState() {
        val bitmap = Bitmap.createBitmap(2, 2, Bitmap.Config.ARGB_8888)

        val result = RadioReducer.reduce(
            state = createInitialRadioUiState(),
            action = RadioAction.PhotoCaptured(bitmap)
        )

        assertSame(bitmap, result.capturedPhoto)
    }
}
