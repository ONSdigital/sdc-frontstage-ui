var gulp = require('gulp'),
	sass = require('gulp-sass'),
	concat = require('gulp-concat'),
	mustache = require('gulp-mustache'),
	webserver = require('gulp-webserver'),
	argv = require('yargs').argv,

	fs = require('fs'),

	config = {
		sassSrc: './sass/*.scss',
		templatesSrc: [
			'./mock-pages/**/*.json',
			'./templates/**/*.mustache',
			'./mock-pages/**/*.mustache'
		],
		outputDir: './dist',
		templatesArr: fs.readdirSync('./mock-pages/src')
	};

var portNumber = process.env.PORT || argv.port || 8181;

console.log(process);

/**
 * Retrieve all partial mustache files
 */
var getPartials = () => {

	var mustachePartialFiles = fs.readdirSync('./templates/partials'),
		mustachePartials = {};

	mustachePartialFiles.forEach((item) => {
		var partial = item.replace('.mustache', '');
		mustachePartials['partials/' + partial] = fs.readFileSync('./templates/partials/' + partial + '.mustache', 'utf8')
	});

	return mustachePartials;
};

/**
 * Compile each page with JSON fixture
 */
config.templatesArr.forEach(file => {

	var page = file.replace('.mustache', '');

	gulp.task('compile:templates:' + page, () => {
		return gulp.src('./templates/html-page.mustache')

			/**
			 * Build mustache template, mix in partials
			 */
			.pipe(mustache('./mock-pages/fixtures/' + page + '.json', {}, Object.assign({
				"content": fs.readFileSync('./mock-pages/src/' + page + '.mustache', 'utf8')
			}, getPartials())))

			.pipe(concat(page + '.html'))
			.pipe(gulp.dest('./mock-pages/dist'));
	});
});


gulp.task('compile:sass', () => {
	return gulp.src(config.sassSrc)
		.pipe(sass())
		.pipe(concat('site.min.css'))
		.pipe(gulp.dest(config.outputDir))
});

var templateTasks = config.templatesArr.map(page => 'compile:templates:' + page.replace('.mustache', ''));

gulp.task('watch:templates', templateTasks, () => {
	gulp.watch(config.templatesSrc, templateTasks);
});


gulp.task('watch:compile:sass', ['compile:sass'], () => {
	gulp.watch(config.sassSrc, ['compile:sass']);
});

gulp.task('webserver', () => {
	gulp.src([
		'./mock-pages/dist/',
		'./dist/',
		'./eq-prototypes/'
	])
	.pipe(webserver({
		//livereload: true,
		//directoryListing: true,
		//open: true,
		host: (process.env.NODE_ENV === 'production' ? '0.0.0.0' : 'localhost'),
		port: portNumber
	}));
});


gulp.task('test', [
	'webserver'
], () => {

});


gulp.task('dev', [
	'compile:sass',
	'watch:compile:sass',
	'watch:templates',
	'webserver'
], () => {

});
