# nibbler
Nibbler is a Python PyOjbC utility for displaying dialogs using .nib files.

## Examples

The best way to play with nibbler is to download this git repo and play with the two example files.

1. Download this repo:

    ```bash
    git clone https://github.com/pudquick/nibbler.git
    cd nibbler/examples
    ```

1. Now you can choose between running the `sweet_example.py` and `sam_example.py` scripts.

## Getting Started

Now that you've seen what nibbler does from the examples you'll likely want to build your own dialog box. To get started you'll need:

* A Mac with Python (fortunately all modern Macs come with this built-in)
* The PyObjC bridge (again comes built-in)
* Xcode (available from the [MAS](https://itunes.apple.com/us/app/xcode/id497799835?mt=12) or [Apple Developer Portal](https://developer.apple.com/xcode/download/more/))

Once the requirements above are meet we're able to create our dialog.

1. Launch Xcode.
1. From your menu bar select `File > New > File...`.
1. For the correct template in Xcode 8, select `macOS` and in `User Interface` select `Window`.
1. Click `Next` and you'll be prompted to save your file. Select a name and location.
1. Now we need to get this file into a `.nib` file. From your menu bar select `File > Export...`. Make sure and change your File Format to `Interface Builder Cocoa NIB`.
1. Now you need to write the python code to connect your elements.

## Tips

* Make sure and give all of your UI elements in Xcode a static identifier. Xcode by default sets identifiers to `Automatic` however that does not work with nibbler.
* Printing your content handles is very helpful: `print n.nib_contents`
* Printing your views can also help with troubleshooting: `print n.views`
* Consult Apple's [macOS Human Interface Guidelines](https://developer.apple.com/library/content/documentation/UserExperience/Conceptual/OSXHIGuidelines/index.html#//apple_ref/doc/uid/20000957) for the authoritative source on the correct usage of UI elements.
* Consult Apple's [Start Developing iOS Apps (Swift):Build a Basic UI](https://developer.apple.com/library/content/referencelibrary/GettingStarted/DevelopiOSAppsSwift/BuildABasicUI.html) for a tutorial on building a UI in Xcode.
