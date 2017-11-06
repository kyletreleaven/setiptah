
https://stackoverflow.com/questions/23340946/gradle-global-build-directory

To setup global build directory you need to add these lines to ~/.gradle/init.gradle:

gradle.projectsLoaded {
    rootProject.allprojects {
        buildDir = "/path/to/build/${rootProject.name}/${project.name}"
    }
}
