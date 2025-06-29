function initFieldsToggle() {
    document.addEventListener('DOMContentLoaded', function () {
        const fieldContainers = document.querySelectorAll('.fields');

        fieldContainers.forEach(container => {
            const tags = container.querySelectorAll('.field-tag:not(.expand-fields)');

            if (tags.length > 5) {
                container.classList.add('collapsed');

                const expandBtn = document.createElement('span');
                expandBtn.className = 'field-tag expand-fields';
                expandBtn.textContent = `+${tags.length - 5} more`;
                expandBtn.style.order = '999';

                expandBtn.addEventListener('click', function () {
                    if (container.classList.contains('collapsed')) {
                        container.classList.remove('collapsed');
                        expandBtn.textContent = 'Show less';
                    } else {
                        container.classList.add('collapsed');
                        expandBtn.textContent = `+${tags.length - 5} more`;
                    }
                });

                container.appendChild(expandBtn);
            }
        });
    });
}

initFieldsToggle();
