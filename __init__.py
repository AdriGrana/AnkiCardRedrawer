from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap

def redraw_card(reviewer):
    """Function to redraw the current card."""
    reviewer.card.load()
    reviewer._showQuestion()

def add_shortcut(reviewer, _old):
    """Function to add a custom shortcut."""
    config = mw.addonManager.getConfig(__name__)
    shortcuts = _old(reviewer)
    custom_shortcut = config.get('shortcut', 'Ctrl+R')  # Default shortcut if not set
    shortcuts.append((custom_shortcut, lambda: redraw_card(reviewer)))
    return shortcuts

def add_redraw_button(reviewer):
    """Function to add a button to the bottom toolbar that triggers card redraw."""
    reviewer.web.eval("""
        (function() {
            if (!document.getElementById('redrawBtn')) {
                // Create a container div if it doesn't exist
                var container = document.getElementById('redrawBtnContainer');
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'redrawBtnContainer';
                    container.style.position = 'fixed';
                    container.style.bottom = '10px';
                    container.style.left = '50%';
                    container.style.transform = 'translateX(-50%)';
                    container.style.zIndex = '1000'; // Ensure it's on top
                    document.body.appendChild(container);
                }

                // Create the button
                var redrawBtn = document.createElement('button');
                redrawBtn.id = 'redrawBtn';
                redrawBtn.textContent = 'Redraw Card';
                redrawBtn.style.margin = '5px';
                redrawBtn.onclick = function() { pycmd('redrawCard'); };
                container.appendChild(redrawBtn);
            }
        })();
    """)

def handle_redraw_card(self, url, _old):
    """Function to handle card redraw when the button is clicked."""
    if url == "redrawCard":
        redraw_card(self)
    else:
        _old(self, url)  # Fixed: Include 'self' when calling _old

def on_reviewer_init(self):
    add_redraw_button(self)

# Wrap the methods at the class level to affect all instances
Reviewer._initWeb = wrap(Reviewer._initWeb, on_reviewer_init, "after")
Reviewer._linkHandler = wrap(Reviewer._linkHandler, handle_redraw_card, "around")
Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, add_shortcut, "around")
