import React from 'react';
import Link from 'next/link';

interface OverlayCardProps {
    slug: string;
    image: string;
    category: string;
    title: string;
}

export default function OverlayCard({ slug, image, category, title }: OverlayCardProps) {
    return (
        <Link href={`/news/${slug}`} className="group relative block overflow-hidden rounded-xl aspect-[1.6/1]">
            <img
                src={image}
                alt={title}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            {/* Gradient Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent"></div>

            {/* Content Container */}
            <div className="absolute inset-x-0 bottom-0 p-5">
                <span className="text-[10px] font-bold text-white/80 uppercase tracking-widest mb-1.5 block drop-shadow-sm">
                    {category}
                </span>
                <h3 className="text-lg font-bold leading-tight text-white group-hover:text-red-400 transition-colors drop-shadow-md">
                    {title}
                </h3>
            </div>
        </Link>
    );
}
