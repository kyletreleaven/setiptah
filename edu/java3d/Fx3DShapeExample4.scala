import javafx.animation.Animation
import javafx.animation.RotateTransition
import javafx.application.Application
import javafx.scene.Group
import javafx.scene.PerspectiveCamera
import javafx.scene.PointLight
import javafx.scene.Scene
import javafx.scene.paint.Color
import javafx.scene.shape.Box
import javafx.scene.shape.CullFace
import javafx.scene.transform.Rotate
import javafx.stage.Stage
import javafx.util.Duration


// TODO(ktreleav): Debug: WARNING: System can't support ConditionalFeature.SCENE3D

object Fx3DShapeExample4 {
    def main(args: Array[String]): Unit = {
        // Java frameworks can be silly, and don't always play nice with Scala patterns:
        // https://stackoverflow.com/questions/12783994/why-is-a-scala-companion-object-compiled-into-two-classesboth-java-and-net-com
        (new Fx3DShapeExample4()
            .launch(args))
    }
}


class Fx3DShapeExample4 extends Application {

    def launch(args: Array[String]): Unit = {
        //println("hello.")
        Application.launch(args: _*)
        //new Fx3DShapeExample4().launch(args: _*)
    }

    override def start(stage: Stage): Unit = {
        // Create a Box.
        val box = new Box(100, 100, 100);
        box.setCullFace(CullFace.NONE);
        box.setTranslateX(250);
        box.setTranslateY(100);
        box.setTranslateZ(400);

        // Create a Camera to view the 3D Shapes
        val camera = new PerspectiveCamera(false);
        camera.setTranslateX(100);
        camera.setTranslateY(-50);
        camera.setTranslateZ(300);

        // Add a Rotation Animation to the Camera
        val rotation = new RotateTransition(Duration.seconds(2), camera);
        rotation.setCycleCount(Animation.INDEFINITE);
        rotation.setFromAngle(0);
        rotation.setToAngle(90);
        rotation.setAutoReverse(true);
        rotation.setAxis(Rotate.X_AXIS);
        rotation.play();

        // Create a red Light
        val redLight = new PointLight();
        redLight.setColor(Color.RED);
        redLight.setTranslateX(250);
        redLight.setTranslateY(-100);
        redLight.setTranslateZ(250);

        // Create a green Light
        val greenLight = new PointLight();
        greenLight.setColor(Color.GREEN);
        greenLight.setTranslateX(250);
        greenLight.setTranslateY(300);
        greenLight.setTranslateZ(300);

        // Add the Box and the Lights to the Group
        val root = new Group(box, redLight, greenLight);

        // Enable Rotation for the Group
        root.setRotationAxis(Rotate.X_AXIS);
        root.setRotate(30);

        // Create a Scene with depth buffer enabled
        val scene = new Scene(root, 300, 400, true);

        // Add the Camera to the Scene
        scene.setCamera(camera);

        // Add the Scene to the Stage
        stage.setScene(scene);

        // Set the Title of the Stage
        stage.setTitle("An Example with a Camera");

        // Display the Stage
        stage.show();           
    }
}
