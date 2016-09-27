# nibbler
Nibbler is a python PyOjbC utility for displaying dialogs using .nib files.

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

* A Mac with python (fortunately all modern Macs come with this built-in)
* The PyObjC bridge (again comes built-in)
* Xcode (available from the [MAS](https://itunes.apple.com/us/app/xcode/id497799835?mt=12) or [Apple Developer Portal](https://developer.apple.com/xcode/downloads/))

Once the requirements above are meet we're able to create our dialog.

1. Launch Xcode.
1. From your menu bar select `File > New > File...`.
1. For your templete scroll down to `macOS > User Interface > Window`.
1. You'll be prompted to save your file. Select a name and location.
1. Now we need to get this file into a `.nib` file. From your menu bar select `File > Export...`. Make sure and change your File Format to `Interface Builder Cocoa NIB`. 
1. Now you need to write the python code to connect your elements.

## Tips

* Make sure and give all of your UI elements in Xcode a static identifier. Xcode by default sets identifiers to `Automatic` however that does work with nibbler.
* Printing your content handles is very helpful: `print n.nib_contents` 
* Printing your views can also help with troubleshooting: `print n.views`
