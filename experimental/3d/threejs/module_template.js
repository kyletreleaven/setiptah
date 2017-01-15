(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined'
		? factory(exports)
		: typeof define === 'function' && define.amd
			? define(['exports'], factory)
			: (factory((global.SNOWGLOBE = global.SNOWGLOBE || {})));
// invoke
}(this, (function (exports) {
	// don't know what this is for...
	'use strict';

	// what's the difference between this and exports?

	function version() {
		return "0.0.0";
	}
	
	exports.version = version;

// end
})));