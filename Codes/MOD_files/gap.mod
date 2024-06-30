NEURON {
	SUFFIX gap
	POINT_PROCESS gap
	NONSPECIFIC_CURRENT i
	RANGE g, i
	POINTER vgap
}
PARAMETER {
	g = 1e-5 (nS)
}
ASSIGNED {
	v (millivolt)
	vgap (millivolt)
	i (nanoamp)
}
BREAKPOINT {
	i = (v - vgap)*g*(1e-3)
}
