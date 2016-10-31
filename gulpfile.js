var gulp = require('gulp'),
	sass = require('gulp-sass'),
	concat = require('gulp-concat'),
	livereload = require('gulp-livereload'),

	config = {
		sassSrc: './sass/*.scss',
		outputDir: './dist'
	};


gulp.task('compile:sass', () => {
	return gulp.src(config.sassSrc)
		.pipe(sass())
		//.pipe(concat('site.min.css'))
		.pipe(gulp.dest(config.outputDir))
		.pipe(livereload());
});

gulp.task('watch:compile:sass', ['compile:sass'], () => {
	gulp.watch(config.sassSrc, ['compile:sass']);
});



gulp.task('dev', [
	'watch:compile:sass'
], () => {
	livereload.listen();
});