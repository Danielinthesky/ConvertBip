package com.example.convertbip.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.hardware.Camera
import android.view.Surface
import android.view.WindowManager
import com.example.convertbip.R

class QRCodeScannerActivity : AppCompatActivity() {

    private var camera: Camera? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.custom_qr_code_scanner)

        val surfaceView = findViewById<SurfaceView>(R.id.qr_code_camera)
        val holder: SurfaceHolder = surfaceView.holder

        holder.addCallback(object : SurfaceHolder.Callback {
            override fun surfaceCreated(holder: SurfaceHolder) {
                // Inicialize a câmera e habilite o foco automático
                try {
                    camera = Camera.open()
                    setCameraDisplayOrientation()

                    camera?.setPreviewDisplay(holder)
                    camera?.startPreview()

                    val params = camera?.parameters
                    if (params?.supportedFocusModes?.contains(Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE) == true) {
                        params.focusMode = Camera.Parameters.FOCUS_MODE_CONTINUOUS_PICTURE
                        camera?.parameters = params
                    }

                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }

            override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
                camera?.stopPreview()
                camera?.startPreview()
            }

            override fun surfaceDestroyed(holder: SurfaceHolder) {
                camera?.release()
                camera = null
            }
        })
    }

    private fun setCameraDisplayOrientation() {
        val rotation = (getSystemService(WINDOW_SERVICE) as WindowManager).defaultDisplay.rotation
        var degrees = 0
        when (rotation) {
            Surface.ROTATION_0 -> degrees = 0
            Surface.ROTATION_90 -> degrees = 90
            Surface.ROTATION_180 -> degrees = 180
            Surface.ROTATION_270 -> degrees = 270
        }

        val info = Camera.CameraInfo()
        Camera.getCameraInfo(Camera.CameraInfo.CAMERA_FACING_BACK, info)

        val result: Int = if (info.facing == Camera.CameraInfo.CAMERA_FACING_FRONT) {
            (info.orientation + degrees) % 360
        } else { // Camera.CameraInfo.CAMERA_FACING_BACK
            (info.orientation - degrees + 360) % 360
        }

        camera?.setDisplayOrientation(result)
    }
}
