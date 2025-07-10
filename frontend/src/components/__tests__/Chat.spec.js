import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Chat from '../Chat.vue';

describe('Chat.vue', () => {
  it('renders chat container', () => {
    const wrapper = mount(Chat);
    expect(wrapper.exists()).toBe(true);
  });
});
