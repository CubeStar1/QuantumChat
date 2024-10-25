<script lang="ts">
	import { onMount } from 'svelte';
	import { Motion } from 'svelte-motion';
	import { cn } from '$lib/utils';

	export let size: number | undefined = 10;
	export let revealSize: number | undefined = 600;
	export let className: string | undefined = undefined;

	let isHovered = false;
	let mousePosition: { x: number | null; y: number | null } = { x: null, y: null };
	let containerRef: HTMLDivElement;
	const updateMousePosition = (e: any) => {
		const rect = containerRef.getBoundingClientRect();
		mousePosition = { x: e.clientX - rect.left, y: e.clientY - rect.top };
	};

	onMount(() => {
		containerRef.addEventListener('mousemove', updateMousePosition);
		return () => {
			if (containerRef) {
				containerRef.removeEventListener('mousemove', updateMousePosition);
			}
		};
	});

	$: maskSize = isHovered ? revealSize : size;
</script>

<Motion
	let:motion
	animate={{
		backgroundColor: isHovered ? 'var(--slate-900)' : 'bg-sky-400'
	}}
>
	<div use:motion bind:this={containerRef} class={cn('relative ', className)}>
		<Motion
			let:motion
			animate={{
				WebkitMaskPosition:
					mousePosition.x &&
					mousePosition.y &&
					maskSize &&
					`${mousePosition?.x - maskSize / 2}px ${mousePosition.y - maskSize / 2}px`,
				WebkitMaskSize: `${maskSize}px`
			}}
			transition={{ type: 'tween', ease: 'backOut', duration: 0.1 }}
		>
			<div
				use:motion
				class="absolute flex h-full w-full items-center justify-center bg-black text-6xl text-white bg-grid-white/[0.2] [mask-image:url(/mask.svg)] [mask-repeat:no-repeat] [mask-size:40px]"
			>
				<div class="absolute inset-0 z-0 h-full w-full bg-black opacity-50" />
				<div
					on:mouseenter={() => {
						isHovered = true;
					}}
					on:mouseleave={() => {
						isHovered = false;
					}}
					class="relative z-20 mx-auto max-w-4xl text-center text-4xl font-bold text-white"
				>
					<slot />
				</div>
			</div>
		</Motion>

		<div class="flex h-full w-full items-center justify-center text-white">
			<slot name="revealText" />
		</div>
	</div>
</Motion>