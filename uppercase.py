# -*- coding: utf-8 -*-
#
# To convert uppercase to lowercase and vice versa
# Created by Wandaymo
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 1.0, 2019/05/11

from anki.hooks import wrap
from aqt.editor import Editor

js_find_replace = """

function getSelectionHtml() {
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}
if (typeof window.getSelection != "undefined") {
    // get selected HTML
    var sel = getSelectionHtml();
    // replace items
    var sel = sel.replace(/%s/g, "%s")
    document.execCommand('insertHTML', false, sel);
    saveField('key');
}
"""

def uppercase(str):
	return up(str.upper())
	
def up(str):
	return str.upper()

def lowercase(str):
	return lc(str.lower())
	
def lc(str):
	return str.lower()

def lowercaseToUppercase(self):
	self.saveNow();
	self.mw.checkpoint(_("Change lowercase to uppercase on selected text"))
	oldL = self.web.selectedText()
	newU = uppercase(oldL)
	self.web.eval(js_find_replace % (oldL, newU))
	self.stealFocus = True;
	self.loadNote();

def uppercaseTolowercase(self):
	self.saveNow();
	self.mw.checkpoint(_("Change uppercase to lowercase on selected text"))
	oldU = self.web.selectedText()
	newL = lowercase(oldU)
	self.web.eval(js_find_replace % (oldU, newL))
	self.stealFocus = True;
	self.loadNote();

def setupButtons(self):
	u = self._addButton("uppercaseButton", lambda s=self: lowercaseToUppercase(self),
		    text=u"A", tip="Change lowercase to uppercase from the selected text  (Ctrl+Shift+a)", key="Ctrl+Shift+a")
	l = self._addButton("uppercaseButton", lambda s=self: uppercaseTolowercase(self),
		    text=u"a", tip="Change uppercase to lowercase from the selected text  (Ctrl+Shift+u)", key="Ctrl+Shift+u")


Editor.lowercaseToUppercase = lowercaseToUppercase
Editor.uppercaseTolowercase = uppercaseTolowercase
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
