/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './apps/**/*.html',
        './apps/**/*.py',
        './config/**/*.py',
    ],
    theme: {
        extend: {
            colors: {
                shell: '#f4efe7',
                'shell-strong': '#ebe2d4',
                ink: '#1f2a2d',
                mist: '#5f6a6c',
                accent: '#1e6b63',
                'accent-strong': '#154d48',
                income: '#20785d',
                expense: '#b1503d',
                wheat: '#d49443',
            },
            boxShadow: {
                shell: '0 24px 70px rgba(44, 58, 60, 0.14)',
                panel: '0 12px 28px rgba(44, 58, 60, 0.08)',
                action: '0 14px 28px rgba(21, 77, 72, 0.18)',
            },
            borderRadius: {
                shell: '30px',
                panel: '24px',
                card: '18px',
                soft: '14px',
            },
            fontFamily: {
                sans: ['Segoe UI', 'Trebuchet MS', 'Verdana', 'sans-serif'],
                serif: ['Georgia', 'Times New Roman', 'serif'],
            },
        },
    },
    plugins: [],
}
