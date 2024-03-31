from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap

def redraw_card(reviewer):
    """Function to redraw the current card."""
    reviewer.card.load()
    reviewer._showQuestion()

def add_shortcut(reviewer, _old):
    """Function to add a custom shortcut."""
    # Load the configuration for the current add-on
    config = mw.addonManager.getConfig(__name__)
    shortcuts = _old(reviewer)
    # Retrieve the custom shortcut key from the config
    custom_shortcut = config['shortcut']
    # Add the custom shortcut
    shortcuts.append((custom_shortcut, lambda: redraw_card(reviewer)))
    return shortcuts

# Wrap the original _shortcutKeys method to include the custom shortcut
Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, add_shortcut, "around")
