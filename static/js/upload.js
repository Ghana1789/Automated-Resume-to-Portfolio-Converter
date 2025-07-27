document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resume');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');
    const uploadButton = document.getElementById('uploadButton');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = document.getElementById('progressBar');
    const uploadError = document.getElementById('uploadError');
    const uploadSuccess = document.getElementById('uploadSuccess');
    const uploadForm = document.getElementById('uploadForm');
    const maxFileSize = 5 * 1024 * 1024; // 5MB

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop zone when file is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('drag-over');
    }

    function unhighlight() {
        dropZone.classList.remove('drag-over');
    }

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFile(file);
    }

    // Handle file selection via input
    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', function() {
        handleFile(this.files[0]);
    });

    function handleFile(file) {
        if (!file) return;

        // Validate file type
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            showError('Please upload a PDF or DOCX file only.');
            return;
        }

        // Validate file size
        if (file.size > maxFileSize) {
            showError('File size exceeds 5MB limit.');
            return;
        }

        // Update file preview
        fileName.textContent = file.name;
        filePreview.style.display = 'flex';
        uploadButton.disabled = false;
        fileInput.files = new DataTransfer().files;
        fileInput.files = new DataTransfer().files;
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        hideError();
    }

    // Remove selected file
    removeFile.addEventListener('click', function() {
        fileInput.value = '';
        filePreview.style.display = 'none';
        uploadButton.disabled = true;
        hideError();
    });

    // Handle form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!fileInput.files[0]) return;

        const formData = new FormData(this);
        const xhr = new XMLHttpRequest();

        // Show progress bar
        uploadProgress.style.display = 'block';
        dropZone.classList.add('uploading');
        uploadButton.disabled = true;

        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
            }
        });

        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                showSuccess('Upload successful! Redirecting...');
                setTimeout(() => window.location.href = '/portfolio', 1500);
            } else {
                showError('Upload failed. Please try again.');
                uploadButton.disabled = false;
            }
            dropZone.classList.remove('uploading');
        });

        xhr.addEventListener('error', function() {
            showError('An error occurred during upload.');
            uploadButton.disabled = false;
            dropZone.classList.remove('uploading');
        });

        xhr.open('POST', uploadForm.action);
        xhr.send(formData);
    });

    function showError(message) {
        uploadError.textContent = message;
        uploadError.style.display = 'block';
        uploadSuccess.style.display = 'none';
    }

    function hideError() {
        uploadError.style.display = 'none';
        uploadSuccess.style.display = 'none';
    }

    function showSuccess(message) {
        uploadSuccess.textContent = message;
        uploadSuccess.style.display = 'block';
        uploadError.style.display = 'none';
    }
});