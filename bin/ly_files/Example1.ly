\version "2.16.0" % necessary for upgrading to future LilyPond versions.

\header{
	title = "Tablature for the song Example1"
	subtitle = ". . . as generated by GuiTabs"
}



\new Staff {
	a, c d e g 
	a c' d' e' 
	g' a' c'' a' 
	g' e' d' c' 
	a g e d c a, 
	 \bar "|."
}

\new TabStaff {
	a, c d e g 
	a c' d' e' 
	g' a' c'' a' 
	g' e' d' c' 
	a g e d c a, 
	 \bar "|."
}

